
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])# fastapi looks for the first match in code if the URL is same in this case only / is present than this func is not matched
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
               search: Optional[str] = ""):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()# we use limit to get user to
    #decide limit and offset to skip. and use contains to see if any searched keyword is in the title or anything you searched for.
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # this code will give post only which match with ownerid 
    return posts# fastapi converts array into json array 

# instead of using all this we are going to use pydantic lib to validate
#@app.post("/createposts")
# def create_post(payLoad: dict = Body(...)): # extract all the fields from body and store in variable payLoad
#     print(payLoad)
#     return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}

# using this to validate 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # define status_code of create
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # to push changes in DB
    new_post = models.Post(owner_id = current_user.id,  **post.dict()) #unpacking dictionary by double asterik so we dont have to writ post.title etc
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

# after this we can use post.title and .content for title and content

# if we remove title or content from body of postman it will generate and error because of required field

# if you define published in body of postman than the value given will be shown and if there is no value default value true will be shown

# if there is nothing in body of rating default value is none and the type is int so and other data type value raises error.



# retrive one post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): # this is a way to validate if it is a int and some other values will give error msg no inter serever msg
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        # dont want to hard code no 404 so we use status of fastapi
        # response.status_code = status.HTTP_404_NOT_FOUND # use response so that we can give 404 not found error when an invalid id is putted
        # return {"message": f"post with id: {id} was not found"}
        # using HTTPeception from fastapi
        #  response: Response (dont have to write this in def now just write below line for above 3)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return  post


# delete a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exists")
    # can use below statment in get_post to show onnly post which matches the user id
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # because there is 204 no content we does not want to give any mesage


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): # to check if request come with right data provided in schema or class above and post store all front end data
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_check = post_query.first()

    if post_check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exists")
    if post_check.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()