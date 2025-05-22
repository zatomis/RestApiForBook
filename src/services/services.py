
# READ (все)
@app.get("/readers/", response_model=List[Reader])
def read_readers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    readers = db.query(ReaderDB).offset(skip).limit(limit).all()
    return readers


# READ (по ID)
@app.get("/readers/{reader_id}", response_model=Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(ReaderDB).filter(ReaderDB.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return db_reader


# UPDATE
@app.put("/readers/{reader_id}", response_model=Reader)
def update_reader(
        reader_id: int,
        reader_data: ReaderUpdate,
        db: Session = Depends(get_db)
):
    db_reader = db.query(ReaderDB).filter(ReaderDB.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    # Обновление только переданных полей
    for key, value in reader_data.dict().items():
        if value is not None:
            setattr(db_reader, key, value)

    # Проверка уникальности email при обновлении
    if reader_data.email and db.query(ReaderDB).filter(
            ReaderDB.email == reader_data.email,
            ReaderDB.id != reader_id
    ).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    db.commit()
    db.refresh(db_reader)
    return db_reader


# DELETE
@app.delete("/readers/{reader_id}", response_model=dict)
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = db.query(ReaderDB).filter(ReaderDB.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    db.delete(db_reader)
    db.commit()
    return {"detail": "Reader deleted"}
