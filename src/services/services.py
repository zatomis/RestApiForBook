

@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Проверка ISBN уникальности
    if book.isbn:
        existing = db.query(BookModel).filter_by(isbn=book.isbn).first()
        if existing:
            raise HTTPException(400, detail="ISBN уже существует")

    db_book = BookModel(**book.dict())
    db.add(db_book)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=str(e))
    db.refresh(db_book)
    return db_book


@app.get("/books", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(BookModel).all()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(404, detail="Книга не найдена")
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(
        book_id: int,
        book_update: BookUpdate,
        db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(404, detail="Книга не найдена")

    # Обновляем только переданные поля
    for field, value in book_update.dict(exclude_unset=True).items():
        if field == 'isbn' and value != book.isbn:
            # Проверка уникальности ISBN
            existing = db.query(BookModel).filter_by(isbn=value).first()
            if existing:
                raise HTTPException(400, detail="ISBN уже существует")
        setattr(book, field, value)

    # Проверка количества экземпляров
    if book.copies < 0:
        raise HTTPException(400, detail="Количество экземпляров не может быть меньше 0")

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(404, detail="Книга не найдена")

    db.delete(book)
    db.commit()
    return {"detail": "Книга удалена успешно"}

