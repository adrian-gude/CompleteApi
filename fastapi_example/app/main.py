from fastapi import FastAPI, Depends, HTTPException
import psycopg2
import os

from .models import Item, ItemCreate

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        database=os.environ.get("POSTGRES_DB", "db"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
    )


@app.post("/items/")
async def create_item(item: ItemCreate):
    connection = get_connection()
    print(connection)
    cursor = connection.cursor()

    try:
        insert_query = "INSERT INTO items (name) VALUES (%s) RETURNING id;"
        cursor.execute(insert_query, (item.name,))
        new_item_id = cursor.fetchone()[0]

        connection.commit()

        new_item = {"item_id": new_item_id, "item_name": item.name}
        return {"message": "Item created", "item": new_item}

    except Exception as e:
        print(f"Error inserting item: {e}")
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error inserting item")

    finally:
        cursor.close()
        connection.close()


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        select_query = "SELECT id, name FROM items WHERE id = %s;"
        cursor.execute(select_query, (item_id,))
        item = cursor.fetchone()

        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"id": item[0], "name": item[1]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading item: {e}")

    finally:
        cursor.close()
        connection.close()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        select_query = "SELECT id FROM items WHERE id = %s;"
        cursor.execute(select_query, (item_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Item not found")

        update_query = "UPDATE items SET name = %s WHERE id = %s;"
        cursor.execute(update_query, (item.name, item_id))
        connection.commit()

        return {"message": "Item updated", "item_id": item_id, "item_name": item.name}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating item: {e}")

    finally:
        cursor.close()
        connection.close()


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        select_query = "SELECT id FROM items WHERE id = %s;"
        cursor.execute(select_query, (item_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Item not found")

        delete_query = "DELETE FROM items WHERE id = %s;"
        cursor.execute(delete_query, (item_id,))
        connection.commit()

        return {"message": "Item deleted", "item_id": item_id}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting item: {e}")

    finally:
        cursor.close()
        connection.close()
