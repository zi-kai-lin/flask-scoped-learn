from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from silver_app.database import db
from silver_app.utils.errors import ConflictException, UnauthorizedException


class AuthService:

    
    @staticmethod
    def register_user(username, email, password, **kwargs):

        from silver_app.user.models import User
        
        try:
            # Create new user
            user = User(username, email, password=password, **kwargs).save()
            
            # Generate JWT token
            print("generating access token")
            access_token = create_access_token(identity=user.id)
            print(access_token)
            return user, access_token
            
        except IntegrityError:
            db.session.rollback()
            raise ConflictException(
                "User with this username or email already exists",
                f"Registration failed for user: {username}"
            )
    
    @staticmethod
    def login_user(username, password):

        from silver_app.user.models import User
        
        # Find user by email
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            raise UnauthorizedException(
                "Invalid Credentials"
            )
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return user, access_token
    
    @staticmethod
    def create_auth_cookies(access_token):

        return {
            "access_token": access_token
        }