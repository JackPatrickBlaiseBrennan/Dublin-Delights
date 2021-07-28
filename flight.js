document.addEventListener('DOMContentLoaded', init, false);

function init() {
    let form_element = document.querySelector('#searcher');
    get_possible_destinations();
    form_element.addEventListener('submit', search_flights, false);
}

function get_possible_destinations(){
  fetch("https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/routes.json", {
  	"method": "GET",
  	"headers": {
  		"x-rapidapi-host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
  		"x-rapidapi-key": "key",
  		"x-access-token": "token"
  	}
  })
  .then(response => {return response.json()})
  .then(data => {return data})
  .catch(err => {console.log(err);})
  .then(add_to_selector);
}

function add_to_selector(response){
  let selector = document.querySelector('#airport');
  for (let u = 0; u < 64964; u+= 1){
    if (response[u]["departure_airport_iata"] === "DUB"){
      let new_option_element = document.createElement('option');
      new_option_element.value = response[u]["arrival_airport_iata"];
      let new_text = document.createTextNode(response[u]["arrival_airport_iata"]);
      new_option_element.appendChild(new_text);
      selector.appendChild(new_option_element);}
   }
}

function search_flights(event){
    event.preventDefault();
    let destination = document.querySelector('#airport');
    let depart = document.querySelector('#depart');
    let url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap?origin=DUB&currency=EUR"
    if (destination.value !== ""){
    url += `&destination=${destination.value}`}
    if (depart.value !== ""){
    url += `&depart_date=${depart.value}`}
    fetch(url, {
	method : "GET",
	headers : {
		"x-rapidapi-host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
		"x-rapidapi-key": "key",
		"x-access-token": "token"
	}
})
.then(response =>{return response.json()})
.then(data => {return data.data})
.catch(err => {console.log(err);})
.then(display_countries);
}

function display_countries(response){
    let login = document.querySelector('#login');
    console.log(login.text)
    let depart = document.querySelector('#depart');
    let destination = document.querySelector('#airport');
    let body_element = document.querySelector('main');
    let wow = ["price", "airline", "flight_number", "departure_at", "return_at"]
    let nice = ["Price : ","Airline : ", "Flight Number : ", "Departs : ", "Returns : "]
    if (response[destination.value] !== undefined){
      for (let i = 0; i < 10; i+= 1) {
          if (response[destination.value][i] !== undefined){
            if (login.text === "Logout"){
              let new_airport_element = document.createElement('input');
              new_airport_element.setAttribute("name","dest");
              new_airport_element.setAttribute("type", "text");
              new_airport_element.setAttribute("id", "dest");
              new_airport_element.setAttribute("class", "disabled");
              new_airport_element.setAttribute("value",destination.value);
              let new_section = document.createElement('section');
              let new_form = document.createElement('form');
              new_form.setAttribute("method","post");
              new_form.setAttribute("action","index.py");
              new_form.setAttribute("target","_blank");
              new_form.appendChild(new_airport_element);
              new_section.appendChild(new_form);
              for (let u = 0; u < wow.length; u+= 1){
                  let new_input_element = document.createElement('input');
                  let new_label_element = document.createElement('label');
                  let new_text_node = document.createTextNode(nice[u]);
                  new_label_element.appendChild(new_text_node);
                  new_label_element.setAttribute("for", wow[u]);
                  new_input_element.setAttribute("class", "disabled");
                  new_input_element.setAttribute("name",wow[u])
                  new_input_element.setAttribute("type", "text");
                  new_input_element.setAttribute("id", wow[u]);
                  new_input_element.setAttribute("value",response[destination.value][i][wow[u]]);
                  new_form.appendChild(new_label_element);
                  new_form.appendChild(new_input_element);
              }
              let new_submit = document.createElement("input");
              new_submit.setAttribute("type","submit");
              new_submit.setAttribute("value","Save");
              new_form.appendChild(new_submit);
              body_element.appendChild(new_section);
            }
            else{
              let new_h1_element = document.createElement('h1');
              let header_text = document.createTextNode(destination.value);
              new_h1_element.appendChild(header_text);
              let new_section = document.createElement('section');
              new_section.appendChild(new_h1_element);
              for (let u = 0; u < wow.length; u+= 1){
                  let new_p_element = document.createElement('p');
                  let new_text_node = document.createTextNode(nice[u] + response[destination.value][i][wow[u]]);
                  new_p_element.appendChild(new_text_node);
                  new_section.appendChild(new_p_element);
              }
              body_element.appendChild(new_section);
            }
          }
      }
    }
      else if (depart.value !== "" || (depart.value === "" && destination.value === "")){
      for (var country in response){
        for (let i = 0; i < 10; i+= 1) {
            if (response[country][i] !== undefined){
              if (login.text === "Logout"){
                let new__element = document.createElement('input');
                new_airport_element.setAttribute("name","dest");
                new_airport_element.setAttribute("type", "text");
                new_airport_element.setAttribute("id", "dest");
                new_airport_element.setAttribute("class", "disabled");
                new_airport_element.setAttribute("value",country);
                let new_section = document.createElement('section');
                let new_form = document.createElement('form');
                new_form.setAttribute("action","index.py");
                new_form.setAttribute("method","post");
                new_form.setAttribute("target","_blank");
                new_form.appendChild(new_airport_element);
                new_section.appendChild(new_form);
                for (let u = 0; u < wow.length; u+= 1){
                    let new_input_element = document.createElement('input');
                    let new_label_element = document.createElement('label');
                    let new_text_node = document.createTextNode(nice[u]);
                    new_label_element.appendChild(new_text_node);
                    new_label_element.setAttribute("for", wow[u]);
                    new_input_element.setAttribute("type", "text");
                    new_input_element.setAttribute("name",wow[u])
                    new_input_element.setAttribute("id", wow[u]);
                    new_input_element.setAttribute("value", response[country][i][wow[u]]);
                    new_input_element.setAttribute("class", "disabled");
                    new_form.appendChild(new_label_element);
                    new_form.appendChild(new_input_element);
                }
                let new_submit = document.createElement("input");
                new_submit.setAttribute("type","submit");
                new_submit.setAttribute("value","Save");
                new_form.appendChild(new_submit);
                body_element.appendChild(new_section);
              }
  else{
                let new_h1_element = document.createElement('h1');
                let header_text = document.createTextNode(country);
                new_h1_element.appendChild(header_text);
                let new_section = document.createElement('section');
                new_section.appendChild(new_h1_element);
                for (let u = 0; u < wow.length; u+= 1){
                    let new_p_element = document.createElement('p');
                    let new_text_node = document.createTextNode(nice[u] + response[country][i][wow[u]]);
                    new_p_element.appendChild(new_text_node);
                    new_section.appendChild(new_p_element);
                }
                body_element.appendChild(new_section);
            }
}
        }
      }
    }
    else {
      let new_h1_element = document.createElement('h1');
      let header_text = document.createTextNode(destination.value);
      new_h1_element.appendChild(header_text);
      let new_section = document.createElement('section');
      new_section.appendChild(new_h1_element);
      let new_p_element = document.createElement('p');
      let new_text_node = document.createTextNode('No Flight From Dublin');
      new_p_element.appendChild(new_text_node);
      new_section.appendChild(new_p_element);
      body_element.appendChild(new_section);
    }
};
