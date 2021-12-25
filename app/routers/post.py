from fastapi import FastAPI, Response, responses, status, HTTPException, Depends, APIRouter
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from typing import Optional, List
from sqlalchemy.sql.functions import  user
from sqlalchemy.orm import Session, session
from sqlalchemy import func
from app import oauth2
from..import models, schemas, utils
from..database import  get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i

# @router.get("/test")
# def login():
#     return {"Hello": "World"}

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
            current_user: int= Depends(oauth2.get_current_User), limit: int = 10, skip: int = 0,search: Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # post=cursor.fetchall()
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # to do join we use join() by default its left inner join in sqlalqmy
    # , group_by for grp by
    # func to get count like functions , func.count(models.Vote.post_id).label("votes")
    posts = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   # print(posts)
    return posts

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"message":f"title:{payload['title']} content:{payload['content']}"}

# @app.post("/posts", status_code= status.HTTP_201_CREATED)
# def create_post(post: Post):
#     post_dict= post.dict()
#     post_dict['id']= randrange(0,10000)
#     my_posts.append(post_dict)
#     return {"data":post_dict} db: Session = Depends(get_db)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), 
                    current_user: int= Depends(oauth2.get_current_User)):
    # cursor.execute("INSERT INTO posts (title, content,published) VALUES(%s,%s,%s) RETURNING *",
    #     ( post.title, post.content, post.published))# will prevent sql injection
    # new_post=cursor.fetchone()
    # conn.commit()   

    #new_post = models.Post(title= post.title,content= post.content,published=post.published)
   # print(current_user.name)
    new_post= models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit() #(variable) new_post: Post
    db.refresh(new_post)
    return new_post

# structure posts carefully  if we have paths matching by chance there might be conflcits
@router.get("/latest/")
def get_latest_post(db:Session = Depends(get_db)):
    #post= my_posts[len(my_posts)-1]
    post=db.query(models.Post).filter().from_self()
    return {"detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db),
            current_user: int= Depends(oauth2.get_current_User)):#, response: Response
    #post = find_post(id)
    # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id)))
    # post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id == id).first()
    post=db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).first()
    0
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with id :{id} was not found"}

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not autherized to perform requested action")
    return post

# uvicorn app.main:app --reload
# d:/FASTAPI/venv/Scripts/activate.bat

@router.delete("/{id}", status_code=HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db),
                current_user: int= Depends(oauth2.get_current_User)):
    # delete post
    # find index of item with required ID
    # my post.pop
    #index= find_index_post(id)
    
    # cursor.execute("DELETE FROM posts WHERE iD= %s returning *",(str(id),))
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    pst = post_query.first()
    if pst == None:
        raise HTTPException(status_code= HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} does not exist")
    
    if pst.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not autherized to perform requested action")

    #my_posts.pop(index)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db),
                current_user: int= Depends(oauth2.get_current_User)):
    #index= find_index_post(id)
    
    # cursor.execute("UPDATE posts SET title=%s, content= %s, published=%s WHERE ID=%s RETURNING *",
    #  (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= HTTP_404_NOT_FOUND, detail= f"post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not autherized to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
    # post_dict= post.dict()
    # post_dict['id']=id
    # my_posts[index]= post_dict
    # return{'data':post_dict}
# post gress library psycopg
# pip install psycopg2
