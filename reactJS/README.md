
Welcome to my react JS squeleton. This will show you how to use it directly for your projects. 

### steps:

#### 1. requirements: 
- you need, of course, to install node (and npm) on your computer.
- you need then to install cookiecutter `npm install cookiecutter` or through python `pip install cookiecutter`

#### 2. project initialization

```
cookiecutter https://github.com/Yameogo123/xxxxxxxx 
```


#### 3. the squeleton 

```
---
├── Makefile               <- simple commande with `make`for complex tasks
├── README.md              <- The top-level README for developers using this project.
├── public                 
│   ├── assets             <- the folder of css, js, images, .... that are directly inserted  
│   │                         in the index.html script
│   └── index.html         <- the entry of all the code. The main html file
├── src
│   ├── controllers        <- (2)- Once you are connected to your API with fetch will help
│   │                           you get, send your data with async that come from services
│   ├── css                <- The css files specific to pages that are in views.
│   ├── hooks              <- The hooks (store, reducer, provider).
│   ├── routing            <- All redirection files organize in 2 (security ones and others)
│   ├── services           <- (1)- will allow you to connect to your APIs (fetch)
│   ├── tests              
│   ├── views              
│   │    ├── security      <- login, signup, .... pages that concern security
│   │    ├── template      <- The template (navbar, sidebar, footer ..) pages
│   │    └── view.home.jsx <- The home page.
│   ├── App.js             <- Will take all the other code into account and send it to index.js.
│   └── index.js           <- this index page will then send the prepared code to the index.html
│
├── .npmrc                 
└── package.json           <- all the necessary packages
---
```

#### 4. how it works

a- Install an environment, the modules

if the make command works:
```
make all-install
```

otherwise
```
npm install
```

b- launch it

if the make command works:
```
make run
```

otherwise
```
npm start
```