var menuLinks=document.querySelectorAll('.global-nav-item');
var currentMenu;
function clickMenuHandler() {
    if (currentMenu){
        currentMenu.classList.remove('menu-active');
    }
    this.classList.add('menu-active');
    currentMenu = this;
    console.log(currentMenu);
    }
for (var i = 0; i<menuLinks.length; i++){
    menuLinks[i].addEventListener('click', clickMenuHandler);
}