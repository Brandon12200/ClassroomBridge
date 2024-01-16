

logInOrOut();


function showLoginForm() {
    document.getElementById('to-blur').style.filter = 'blur(3px)';
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('classForm').style.display = 'none';
    document.getElementById('studentForm').style.display = 'none';
}

function showRegisterForm() {
    document.getElementById('to-blur').style.filter = 'blur(3px)';
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('classForm').style.display = 'none';
}

function goBack() {
    document.getElementById('to-blur').style.filter = 'blur(0px)';
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('classForm').style.display = 'none';
}

document.addEventListener('click', function(event) {
    var overlay = document.getElementById('overlay');
    var loginForm = document.getElementById('loginForm');
    var registerForm = document.getElementById('registerForm');
    var newClassForm = document.getElementById('classForm');

    if (!loginForm.contains(event.target) && !registerForm.contains(event.target) && overlay.contains(event.target) && !newClassForm.contains(event.target)) {
        goBack();
    }
});

function isLoggedIn() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            if (data.is_authenticated) {
                var loginUrl = document.getElementById('view-classes-button').getAttribute('data-login-url');
                window.location.href = loginUrl;
            } else {
                showLoginForm();
            }
        })
        .catch(error => {
            console.error('Error fetching login status:', error);
        });
}

function logInOrOut() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            if (data.is_authenticated) {
                document.querySelector('.login-and-register').style.display = 'none';
                document.querySelector('.logout').style.display = 'block';
            } else {
                document.querySelector('.login-and-register').style.display = 'block';
                document.querySelector('.logout').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching login status:', error);
        });
}

function showNewClassForm() {
    document.getElementById('to-blur').style.filter = 'blur(3px)';
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('classForm').style.display = 'block';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
}