import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.models import Candidate, Job, AnalysisResult

class AIEngine:
    def __init__(self):
        # Initializing local open-source models
        # These will automatically download to local cache on first boot, then run 100% offline
        self.bi_encoder = SentenceTransformer('BAAI/bge-small-en-v1.5')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
    def _prepare_candidate_text(self, candidate: Candidate) -> str:
        """
        Combines candidate profile fields into a single rich text representation
        for high-quality dense vector embedding extraction.
        """
        components = [
            f"Skills: {candidate.skills or 'None'}",
            f"Experience: {candidate.experience_years or 0} years",
            f"Education: {candidate.education or 'None'}",
            f"Projects: {candidate.projects or 'None'}",
            f"Summary: {candidate.resume_summary or 'None'}",
            f"Certifications: {candidate.certifications or 'None'}"
        ]
        return " | ".join(components)

    def run_matching_pipeline(self, db: Session, job_id: int) -> List[Dict[str, Any]]:
        """
        Executes the entire semantic discovery loop:
        1. Generates dense embeddings for the Job Description and all Candidates (Phase 6).
        2. Populates a temporary local FAISS Index (Phase 7).
        3. Queries index via Cosine Similarity + CrossEncoder Reranking (Phase 8 & 9).
        """
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job with ID {job_id} not found.")

        candidates = db.query(Candidate).all()
        if not candidates:
            return []

        # Phase 6: Generate Embeddings
        job_text = f"Job Title: {job.title} | Requirements: {job.description}"
        job_embedding = self.bi_encoder.encode([job_text], convert_to_numpy=True)
        
        candidate_texts = [self._prepare_candidate_text(c) for c in candidates]
        candidate_embeddings = self.bi_encoder.encode(candidate_texts, convert_to_numpy=True)

        # Phase 7: Vector Indexing via FAISS
        dimension = candidate_embeddings.shape[1]
        # Using IndexFlatIP (Inner Product) with normalized vectors calculates Cosine Similarity
        faiss.normalize_L2(candidate_embeddings)
        faiss.normalize_L2(job_embedding)
        
        index = faiss.IndexFlatIP(dimension)
        index.add(candidate_embeddings)

        # Phase 8: Semantic Search (Retrieve top candidates)
        # We search for all candidates to rank the entire batch
        k = len(candidates)
        scores, indices = index.search(job_embedding, k)

        retrieved_results = []
        for rank, idx in enumerate(indices[0]):
            candidate_idx = int(idx)
            initial_score = float(scores[0][rank])
            retrieved_results.append({
                "candidate": candidates[candidate_idx],
                "bi_encoder_score": initial_score
            })

        # Phase 9: Cross-Encoder Reranking
        # Pairs are formed as [Job Description, Candidate Text]
        rerank_pairs = [[job_text, self._prepare_candidate_text(res["candidate"])] for res in retrieved_results]
        rerank_scores = self.reranker.predict(rerank_pairs)

        # Normalize CrossEncoder scores to a 0-100 scale safely using a sigmoid approximation
        final_ranked_candidates = []
        for idx, res in enumerate(retrieved_results):
            raw_rerank_score = float(rerank_scores[idx])
            # Mapping standard cross encoder logit ranges to percentage values
            normalized_score = round(100 / (1 + np.exp(-raw_rerank_score)), 2)
            # Guarantee confidence boundings
            confidence_score = round((res["bi_encoder_score"] * 40) + (normalized_score * 0.6), 2)
            if confidence_score > 100: confidence_score = 100.0

            final_ranked_candidates.append({
                "candidate": res["candidate"],
                "overall_score": normalized_score,
                "ai_confidence": confidence_score
            })

        # Sort the final candidates list by the high-precision reranked score
        final_ranked_candidates.sort(key=lambda x: x["overall_score"], reverse=True)
        return final_ranked_candidates

# Instantiate the singleton engine to avoid reloading models on every API hit
ai_pipeline_engine = AIEngine()