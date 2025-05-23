from datetime import datetime

from fastapi import HTTPException
from src.schemas.books import BookUpdateDTO
from src.schemas.services import BorrowDTO
from src.services.base import BaseService

class BorrowService(BaseService):
    async def borrow_book(self, borrow_data: BorrowDTO):
        book = await self.db.books.get_one_or_none(id=borrow_data.book_id)
        reader = await self.db.readers.get_one_or_none(id=borrow_data.reader_id)
        bk = book.copies

        if not book or not reader:
            raise HTTPException(status_code=404, detail="Книга или читатель - не найдены")

        if book.copies <= 0:
            raise HTTPException(status_code=400, detail="No available copies")

        borrowed_count = 0
        borrowed_books_reader = await self.db.borrowed_books.get_filtered(reader_id=borrow_data.reader_id)
        for bc in borrowed_books_reader:
            if not bc.return_date:
                borrowed_count += 1

        print(f"borrowed_count {borrowed_count}")
        if borrowed_count >= 3:
            raise HTTPException(status_code=400, detail="Превышен лимит на выдачу книг")

        await self.db.borrowed_books.add(borrow_data)
        await self.db.commit()

        bk -= 1
        new_book = BookUpdateDTO(
            copies=bk,
        )
        await self.db.books.edit(new_book, exclude_unset=True, id=book.id)
        await self.db.commit()


    async def return_book(self, borrow_data: BorrowDTO):
        book = await self.db.books.get_one_or_none(id=borrow_data.book_id)
        reader = await self.db.readers.get_one_or_none(id=borrow_data.reader_id)
        bk = book.copies

        if not book or not reader:
            raise HTTPException(status_code=404, detail="Книга или читатель - не найдены")

        bid = 0
        borrowed_books_reader = await self.db.borrowed_books.get_filtered(reader_id=borrow_data.reader_id, book_id=borrow_data.book_id)
        for bc in borrowed_books_reader:
            if not bc.return_date:
                bid = bc.id
                break
        if not bid:
            raise HTTPException(status_code=404, detail="Нельзя вернуть книгу, которая не была выдана этому читателю или уже возвращена")
        else:
            bk += 1
            new_book = BookUpdateDTO(copies=bk,)
            await self.db.books.edit(new_book, exclude_unset=True, id=book.id)
            await self.db.commit()

            br = await self.db.borrowed_books.get_one(id=bid)
            br.return_date = datetime.now()
            await self.db.commit()





