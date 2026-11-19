from datetime import timedelta

from odoo import fields


def run_demo(env):
    books = env["library.book"]
    loans = env["library.loan"]
    today = fields.Date.context_today(loans)

    author = "Тарас Шевченко"
    by_author = books.search([("author", "=", author)])
    print(f"1. Книги автора {author} ({len(by_author)}):")
    print("   " + ", ".join(by_author.mapped("name")))

    book = env.ref("library_rental.book_kobzar")
    active_copies = loans.search([
        ("copy_id", "in", book.copy_ids.ids),
        ("state", "=", "active"),
    ]).mapped("copy_id")
    available_copies = book.copy_ids - active_copies
    print(f"2. Вільні примірники книги «{book.name}»: {len(available_copies)}")
    print("   " + ", ".join(available_copies.mapped("inventory_number")))

    overdue = loans.search([("state", "=", "active"), ("due_date", "<", today)])
    print(f"3. Прострочені активні видачі станом на {today}: {len(overdue)}")
    for loan in overdue:
        print(f"   {loan.copy_id.inventory_number} | {loan.member_id.name} | до {loan.due_date}")

    if not available_copies:
        raise ValueError("Для демонстрації потрібен хоча б один вільний «Кобзар».")

    copy = available_copies[0]
    member = env.ref("library_rental.member_maksym")
    loan = loans.create({
        "copy_id": copy.id,
        "member_id": member.id,
        "due_date": today + timedelta(days=7),
    })
    print(f"4. create(): видача #{loan.id} | {copy.inventory_number} | {loan.state}")
    loan.write({"state": "returned", "return_date": today})
    print(f"   write(): видача #{loan.id} | {loan.state} | повернено {loan.return_date}")


run_demo(env)
env.cr.rollback()
print("Демонстраційну видачу відкочено. Початкові дані збережено.")
