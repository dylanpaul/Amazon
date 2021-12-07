VIDEO: our video is uploaded as a mp3 file

Isabella (icg2)- I worked primarily on the account information and seller view pages of our Website. 
The account information page shows the information about a certain user. It gives them the ability to 
edit their email, firstname, last name, address and balance. It also shows them all their recent purchases.
From this page, if the user is a seller they are able to access the seller view page. This page shows the 
seller a list of their products giving them the ability to add or delete a product. It also gives them the 
ability to edit the price, inventory and the availability status of the product. Furthermore, on this page 
the seller can see the order history of past orders with the ability to mark orders as fulfilled. I also 
notably added the sorting and search features to the home page. Outside of these pages I worked on features 
of various pages. 

Christian (cgg18)- I worked mostly on the cart features and functions that were necessary to successfully 
complete a purchase. The user can add a specific quantity of a product from a detailed products page or a 
sellers page. The code also checks to ensure that the quantity they enter is valid, meaning it is an integer 
greater than 0 and there is enough stock for that quantity. Once items are added to the cart, the cart page 
displays the product name, seller name, unit price, image, quantity to be purchased, the current stock of that
product, and the total cost of the purchase next to the user’s balance. The user can then choose to keep 
adding more items to the cart or complete their purchase. Completing the purchase takes the user to an order
summary page, showing them information about the products they just bought, their old balance, the total cost,
and their new balance. This checkout feature has several important implementations. First, it checks each 
item to ensure that the quantities selected are still less than or equal to the stock available. It also 
checks to make sure the user has enough balance. If either check fails, an error message is displayed, and 
the purchase cannot be completed until the issue is resolved. If these checks pass, then the purchase is 
completed. Each product is added to the purchases table to be stored in past purchases. Checking out also 
decrements the stock of the items purchased and sets any that become 0 to unavailable, decrements the users 
balance, increases the sellers balance for each product, and ultimately clears the cart. Finally, a detailed
overview of that purchase can be seen from the user information page under an purchase ID. All of these 
features are fully functional.
 

Dylan (dhp14)- I worked primarily on setting up the database design and data generation, registration ability
of users, the balance system used throughout the site, the inclusion of images in the site, the seller page, 
and the addition of products from sellers. For the database design, we consistently modified the structure of
our tables to meet our needs and have settled on the design seen in this final submission. Additionally, for 
the data generation, I populated CSV files with ‘fake’ information from the ‘faker’ module, so that the website
had data upon initial running. For the registration ability of users, I ensured that the email address was 
unique and that the user can specify if they are a ‘seller’ or not. Upon successful registration, their 
password is hashed and their information is stored in the database so they can then proceed to log in. 
If the user specifies that they are a seller, then in their account information, they will have the ability 
to add products. Additionally, I worked on creating the balance system used throughout the site. This gives 
users the ability to add or withdraw to their balance and have their balance increase or decrease depending 
on if someone buys their product or if they buy a product themselves. I also ensured that images of products
could be added to the site. First, I populated the database with  ‘fake’ images and then ensured that these
product images would be seen on the home page as well as in the cart and detailed products page. Also, 
images are able to be added to a product by a seller if the seller provides a proper URL for the image. 
All of the features described are fully functional. Due to the nature of the project and the fact that we 
were down to 3 members, the team worked on many different features and solved problems as they arose. 
