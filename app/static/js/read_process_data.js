var menu_couner_el = document.getElementById('number_of_menus')
if (menu_couner_el == undefined ){
    MENU_COUNTER = 1
} else {
    MENU_COUNTER = parseInt(menu_couner_el.innerHTML)
}


function read_data() {
    if (!(check_all_input())) {
        alert("Provjerite sve unose!")
        return
    }

    document.getElementById("prepareAndSendBtn").disabled = true;
    setTimeout(function() {
        document.getElementById("prepareAndSendBtn").disabled = false;
    }, 3500);


    var food = 
    {  
        "croatian":{  
           "tip":"",
           "menus":[],
           "pojedinacna-jela":"",
           "prilozi":"",
           "marende":""
        },
        "english":{  
           "type":"",
           "menus":[],
           "extra-meals":"",
           "side-dishes":"",
           "brunches":""
        },
        "menus-no": 0
    }


    if(document.getElementById('type_lunch').checked) {
        food['croatian']['tip'] = 'Rucak'
        food['english']['type'] = 'Lunch'
      }else if(document.getElementById('type_dinner').checked) {
        food['croatian']['tip'] = 'Vecera'
        food['english']['type'] = 'Dinner'
      }

    var menu_div = document.getElementById("menus")
    var all_menus = menu_div.getElementsByClassName("menu")
    food['menus-no'] = all_menus.length

    for (var i = 0; i < all_menus.length; ++i) {
        var cro = all_menus[i].getElementsByClassName("textarea_cro")[0]
        cro = cro.value.replace('\n\n', '')
        food['croatian']['menus'].push(cro)

        var eng = all_menus[i].getElementsByClassName("textarea_eng")[0]
        eng = eng.value.replace('\n\n', '')
        food['english']['menus'].push(eng)
    }

    var extra_meals = document.getElementById("extraMeals")
    var cro = extra_meals.getElementsByClassName("textarea_cro")[0]
    cro = cro.value.replace('\n\n', '')
    food['croatian']['pojedinacna-jela'] = cro
    var eng = extra_meals.getElementsByClassName("textarea_eng")[0]
    eng = eng.value.replace('\n\n', '')
    food['english']['extra-meals']= eng

    var sideMeals = document.getElementById("sideMeals")
    var cro = sideMeals.getElementsByClassName("textarea_cro")[0]
    cro = cro.value.replace('\n\n', '')
    food['croatian']['prilozi'] = cro
    var eng = sideMeals.getElementsByClassName("textarea_eng")[0]
    eng = eng.value.replace('\n\n', '')
    food['english']['side-dishes']= eng

    var brunches = document.getElementById("brunches")
    var cro = brunches.getElementsByClassName("textarea_cro")[0]
    cro = cro.value.replace('\n\n', '')
    food['croatian']['marende']= cro
    var eng = brunches.getElementsByClassName("textarea_eng")[0]
    eng = eng.value.replace('\n\n', '')
    food['english']['brunches']= eng

    send_to_processing(food)
}

function send_to_processing(jfood) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/processing', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        food: jfood
    }));
    console.log(xhr.response, xhr.status)
    var response = JSON.parse(xhr.response)
    console.log(response)
    window.location.href = response['redirect']
}


function create_menu_cards() {

    // <textarea rows="5" class="textarea_card textarea_eng"></textarea>
    var eng_textarea = document.createElement("textarea")
    eng_textarea.setAttribute("rows", "5")
    eng_textarea.setAttribute("class", "textarea_card textarea_eng")

    var cro_textarea = document.createElement("textarea")
    cro_textarea.setAttribute("rows", "5")
    cro_textarea.setAttribute("class", "textarea_card textarea_cro")

    var eng_title = document.createElement('h5')
    eng_title.setAttribute('class', 'card-header')

    var cro_title = document.createElement('h5')
    cro_title.setAttribute('class', 'card-header')

    eng_title.innerText = "Menu " + MENU_COUNTER.toString()
    cro_title.innerText = "Meni " + MENU_COUNTER.toString()

    var eng_card_body = document.createElement('div')
    eng_card_body.setAttribute('class', 'card-body')

    var cro_card_body = document.createElement('div')
    cro_card_body.setAttribute('class', 'card-body')

    eng_card_body.appendChild(eng_textarea)
    cro_card_body.appendChild(cro_textarea)

    var cro_card = document.createElement('div')
    cro_card.setAttribute('class', 'card')

    var eng_card = document.createElement('div')
    eng_card.setAttribute('class', 'card')

    cro_card.appendChild(cro_title)
    cro_card.appendChild(cro_card_body)
    
    eng_card.appendChild(eng_title)
    eng_card.appendChild(eng_card_body)

    console.log(cro_card)
    console.log(eng_card)

    return [cro_card, eng_card]
}

function add_menu() {
    MENU_COUNTER += 1;

    var menu_div = document.getElementById("menus")

    var new_menu = document.createElement('div')
    new_menu.setAttribute("class", "row menu")

    var cro_col = document.createElement('div')
    cro_col.setAttribute('class', 'col')

    var eng_col = document.createElement('div')
    eng_col.setAttribute('class', 'col')

    var cards = create_menu_cards()

    cro_col.appendChild(cards[0])
    eng_col.appendChild(cards[1])

    new_menu.appendChild(cro_col)
    new_menu.appendChild(eng_col)

    menu_div.appendChild(new_menu)
}

function remove_menu() {
    var menu_div = document.getElementById("menus")
    var all_menus = menu_div.getElementsByClassName("menu")


    if (all_menus.length > 1)  {
        menu_div.removeChild(all_menus[MENU_COUNTER - 1])
        MENU_COUNTER -= 1;
    }    
}

function clear_everything() {
    var textareas = document.getElementsByClassName("textarea_card")

    for (var i = 0; i < textareas.length; ++i) {
        textareas[i].value = ''
    }

    if (MENU_COUNTER > 1) {
        for(var i = 0; i < MENU_COUNTER; ++i) {
            remove_menu()
        } 
    }
}

function check_all_input() {
        var textareas = document.getElementsByClassName("textarea_card");
    
        for (var i = 0; i < textareas.length; ++i) {
            if (textareas[i].value.length < 4) {
                return false;
            }
        }
        return true;
}

document.addEventListener('paste', function (evt) {
    console.log('ok')
    clipdata = evt.clipboardData || window.clipboardData;
    data = clipdata.getData('text/plain')
    data = data.replace('"', '')
    data = data.replace("'", '')
    data = data.replace('\t', '')
    data = data.replace('\r\n\r\n', '')
    data = data.replace('\n\n', '')

    evt.target.value = evt.target.value.replace(/[\r\n]+/g, "").trim();

});