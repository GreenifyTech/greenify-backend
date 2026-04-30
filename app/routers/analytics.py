from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from app.database import get_db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.analytics_logs import SearchLog, DiagnosticLog
from app.models.user import User
from typing import List, Dict, Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

def get_date_filter(days: int):
    if days == 0: return None # All time
    return datetime.utcnow() - timedelta(days=days)

@router.get("/summary")
def get_analytics_summary(days: int = 7, db: Session = Depends(get_db)):
    date_limit = get_date_filter(days)
    
    orders_query = db.query(Order).filter(Order.status != "CANCELLED")
    if date_limit:
        orders_query = orders_query.filter(Order.created_at >= date_limit)
    
    total_sales = db.query(func.sum(Order.total_amount)).filter(Order.status != "CANCELLED")
    if date_limit:
        total_sales = total_sales.filter(Order.created_at >= date_limit)
    
    total_sales = total_sales.scalar() or 0
    total_orders = orders_query.count()
    total_users = db.query(func.count(User.id)).count()
    total_products = db.query(func.count(Product.id)).count()

    return {
        "total_sales": round(total_sales, 2),
        "total_orders": total_orders,
        "total_users": total_users,
        "total_products": total_products
    }

@router.get("/top-medicines")
def get_top_medicines(days: int = 7, db: Session = Depends(get_db)):
    date_limit = get_date_filter(days)
    
    query = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("total_sold"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Product.product_type == "MEDICINE")
        .filter(Order.status != "CANCELLED")
    )
    
    if date_limit:
        query = query.filter(Order.created_at >= date_limit)
        
    top_selling = query.group_by(Product.id).order_by(desc("total_sold")).limit(5).all()
    
    return [{"name": name, "value": total_sold} for name, total_sold in top_selling]

@router.get("/top-searches")
def get_top_searches(days: int = 7, db: Session = Depends(get_db)):
    date_limit = get_date_filter(days)
    
    query = db.query(SearchLog.query, func.count(SearchLog.id).label("count")).filter(SearchLog.source == "encyclopedia")
    
    if date_limit:
        query = query.filter(SearchLog.created_at >= date_limit)
        
    top_searches = query.group_by(SearchLog.query).order_by(desc("count")).limit(6).all()
    
    return [{"name": query, "value": count} for query, count in top_searches]

@router.get("/recent-diagnostics")
def get_recent_diagnostics(days: int = 7, db: Session = Depends(get_db)):
    date_limit = get_date_filter(days)
    query = db.query(DiagnosticLog)
    
    if date_limit:
        query = query.filter(DiagnosticLog.created_at >= date_limit)
        
    logs = query.order_by(desc(DiagnosticLog.created_at)).limit(10).all()
    return logs

@router.get("/sales-trend")
def get_sales_trend(days: int = 7, db: Session = Depends(get_db)):
    date_limit = get_date_filter(days)
    
    query = (
        db.query(func.date(Order.created_at).label("date"), func.sum(Order.total_amount).label("total"))
        .filter(Order.status != "CANCELLED")
    )
    
    if date_limit:
        query = query.filter(Order.created_at >= date_limit)
        
    sales = query.group_by(func.date(Order.created_at)).order_by(func.date(Order.created_at)).all()
    
    return [{"date": str(date), "amount": float(total)} for date, total in sales]
