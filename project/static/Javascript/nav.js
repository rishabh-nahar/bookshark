prev_anchor = document.getElementById('search_achor_link').href
function on_search_q(){
    book_cat = document.querySelector('.book-category-select').value;
    search_q = document.querySelector('.search_q_input').value;
    document.getElementById('search_achor_link').href = prev_anchor + "?search_query=" + search_q;
}


function show_navbar(){
    document.getElementById('hidden_nav').classList.toggle('hide-nav-container');
    document.getElementById('hamburger_container').classList.toggle('hamburger-container');
    document.getElementById('logo').classList.toggle('logo-on-ham-clicked');
    document.getElementById('line1').classList.toggle('line1');
    document.getElementById('line2').classList.toggle('line2');
    document.getElementById('line3').classList.toggle('line3');
}