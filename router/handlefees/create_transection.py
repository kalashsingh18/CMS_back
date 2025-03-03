from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import teacher  # Import Models
from schemas.schemas import Createtransection  # Import Schema
from dependencies import get_db 