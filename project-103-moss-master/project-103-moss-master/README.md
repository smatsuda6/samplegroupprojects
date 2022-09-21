# project-103-moss

Ever wanted a way to find classmates who have a particular skill and are willing to help out folks in need? In this project we are building a web app that students can use to create an account, post information about themselves, including what skills/expertise they have. Other students will then be able to  search on "tags" that will match up studnets with people that may be able to help.

The website is hosted on heroku here: https://moss-skillshare.herokuapp.com

Setup:
1. pip3 install Django
2. pip3 install python-social-auth[django]
3. pip3 install python-jose
4. pip3 install django-crispy-forms


Run:
In projects root folder run
	python3 mangage.py runserver
	
## How to use our website!
The homepage has a carousel of stock-images which is a hyperlink to login. You can login by clicking on the images or by just clicking on the _Login_ button. After you login with your Gmail account, you are brought to your _Post Feed_. This is where you will see the posts from the users you follow and also create a new post yourself. You can sort these posts by various critearias from the **Sort by** drop down. At the top of each page, you will see the navigation bar. The title **MOSS - Student Skill Sharing** is button that you can press to go back to the main timeline page. The bar next to it is the _search bar_, where you can search for posts or users. Next to that is the drop down menu regarding anything related to your profile and your notifications. 
### Creating a Post
Once you clicked the _Create a Post_ button, you will be taken to a new page where you will be able to enter a **Title** and a **Body** for your post. You can click **Submit Post** which will take you to the page of your new post, where you can see the comments, likes and also edit or delete your post.
### Searching
The search engine works like keyword querying. Your search text will be parsed into words and it will be queried over the posts and users database to find anything related to your search text. You can choose to click on a specific post or user, which is highlighted in blue. 
### My Account(Profile pages)
If you click on _My account_ from the profile drop down menu, you will see your profile page. Here, you can see how many users you are following and the count of users following you. At any profile page you browse, you will see a timeline of all the posts that specific user has posted, with meta data. You can choose to follow/unfollow users from their profile pages.
### Notifications
You will be notified when a user follows you, comments on your post or likes any one of your posts. You can see all of your notifications by clicking on **My notifications** from the drop down menu. You will also have a red indicator for unread notifications next to your username.
### Logout
You can logout from the drop down menu.
