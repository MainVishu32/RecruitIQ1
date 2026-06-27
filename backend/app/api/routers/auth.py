from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserLogin, Token
from app.core.security import verify_password, create_access_token, get_password_hash
from app.api.deps import get_db
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    # Auto-registration for hackathon demonstration purposes. 
    # If the user doesn't exist, we create them on the fly.
    if not user:
        hashed_pw = get_password_hash(user_credentials.password)
        user = User(email=user_credentials.email, hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}