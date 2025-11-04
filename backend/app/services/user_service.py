from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.user import User
from app.core.security import get_password_hash, verify_password

class UserServices:

    @staticmethod
    def get_user_id(db: Session, user_id: int) -> User:
        """get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
        update_data = user_data.model_dump(exclude_unset=True)

        if "username" in update_data and update_data['username'] != user.username:
            if db.query(User).filter(User.username == update_data["username"].lower()).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="username already exists"
                )
            update_data['username'] = update_data['username'].lower()

        if 'email' in update_data and update_data['email'] != user.email:
            if db.query(User).filter(User.email == update_data['email']).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="email alrady registered"
                )
        
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user:User, old_password: str, new_password:str)->None:
        if not verify_password(old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incorrect password"
            )
        
        if verify_password(new_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new password cant be same as old password"
            )
        user.password = get_password_hash(new_password)

        db.add(user)
        db.commit()
        db.refresh(user)

    @staticmethod
    def delete_user(db: Session, user: User) -> None:

        db.delete(user)
        db.commit()
        

        