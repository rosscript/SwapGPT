var currencies = {};

function typeMessage(message, container) {
    var i = 0;
    var interval = setInterval(function() {
        if (i < message.length) {
            container.append(message[i]);
            i++;
        } else {
            clearInterval(interval);
        }
    }, 20); // Imposta l'intervallo di tempo per ciascuna lettera qui
}

$(document).ready(function() {
    var modal = document.getElementById("crypto-modal");
    var closeButton = document.getElementsByClassName("close")[0];
    
    function openModal() {
        modal.style.display = "block";
        modal.classList.remove("closed");
        $(modal).find(".modal-content").addClass("slide-in").removeClass("slide-out");
    }
    
    function closeModal() {
        modal.classList.add("closed");
        $(modal).find(".modal-content").removeClass("slide-in").addClass("slide-out");
        
        setTimeout(function () {
            modal.style.display = "none";
            $(modal).find(".modal-content").removeClass("slide-out");
        }, 300);
    }
    
    // Chiudi il modal cliccando sul pulsante di chiusura
    closeButton.onclick = function() {
        closeModal();
    };
    
    // Chiudi il modal cliccando al di fuori del contenuto del modal
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    };

    // Aggiungi un messaggio preimpostato alla tua area di risposta
    var initialMessage = "Hi, welcome on SwapGPT. I can help you swap cryptocurrencies! Ask me anything or use the buttons below to get started.";
    var initialMessageContainer = $("<div></div>").css({
        "background-color": "#272727",
        "color": "white",
        "padding": "5px",
        "border-radius": "5px",
        "margin-top": "10px"
    });
    $("#response-container").append(initialMessageContainer);
    typeMessage(initialMessage, initialMessageContainer);

    // Crea i pulsanti
    var button1 = $("<button>📄 Availability</button>").attr('id', 'availability-button').css({
        "padding": "10px",
        "margin-right": "10px",
        "background-color": "#545454",
        "color": "#e6e6e6",
        "border-radius": "5px",
        "cursor": "pointer",
        "border": "none"
    });

    var button2 = $("<button>✍🏻 New Order</button>").attr('id', 'neworder-button').css({
        "padding": "10px",
        "margin-right": "10px",
        "background-color": "#545454",
        "color": "#e6e6e6",
        "border-radius": "5px",
        "cursor": "pointer",
        "border": "none"
    });

    var button3 = $("<button>ℹ️ Order Info</button>").attr('id', 'orderinfo-button').css({
        "padding": "10px",
        "background-color": "#545454",
        "color": "#e6e6e6",
        "border-radius": "5px",
        "cursor": "pointer",
        "border": "none"
    });

    // Crea un contenitore per i pulsanti e aggiungi i pulsanti al contenitore
    var buttonContainer = $("<div></div>").css({
        "display": "flex",
        "justify-content": "left",
        "margin-top": "30px"
    });
    buttonContainer.append(button1, button2, button3);

    $("#user-message").keyup(function(event) {
        if (event.keyCode === 13) { // 13 è il codice per il tasto Invio
            event.preventDefault();
            $("#message-form button[type='submit']").click();
        }
    });
    
    // Aggiungi il contenitore dei pulsanti all'area di risposta
    initialMessageContainer.after(buttonContainer);

    $("#message-form button[type='submit']").click(function(event) {
        event.preventDefault();
        var userMessage = $("#user-message").val();

        $.ajax({
            url: "/process_message",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "message": userMessage }),
            beforeSend: function() {
                $("#typing-indicator").removeClass("hidden");
                // Hide the last response if any.
                $("#response-container div:not(#typing-indicator)").remove();
            },
            success: function(response) {
                $("#typing-indicator").addClass("hidden");
                
                // Se i dati dell'ordine sono presenti nella risposta
                if (response.order_data) {
                    console.log(response.order_data);
                    var orderData = JSON.parse(response.order_data);
                    
                    // Crea un nuovo div per i dati dell'ordine
                    var orderDataDiv = $("<div></div>")
                        .addClass("order-data-div")
                        .css({
                            "display": "block",
                            "background-color": "white",
                            "color": "#272727",
                            "padding": "10px",
                            "border-radius": "5px",
                            "margin-top": "10px",
                            "text-align": "left"
                        });
            
                    if (orderData.data) {
                        // Crea i tre sottodiv
                        var topDiv = $("<div></div>")
                            .addClass("top-div")
                            .css({
                                "margin-bottom": "10px"
                            });
            
                        var middleDiv = $("<div></div>").addClass("middle-div").css({
                            "border-bottom": "1px solid #ddd",
                            "padding-bottom": "10px",
                            "margin-bottom": "10px"
                        });
            
                        var bottomDiv = $("<div></div>").addClass("bottom-div").css({
                            "padding-top": "10px",
                        });
            
                        var orderIdSpan = $('<span></span>').text('OrderID: ' + orderData.data.id);
                        topDiv.html(orderIdSpan);
            
                        var bottomInfo = 'Send ' + orderData.data.from.amount + ' ' + orderData.data.from.symbol + ' to ' + orderData.data.from.address + '<br><br>' +
                            'Receive ' + orderData.data.to.amount + ' ' + orderData.data.to.symbol + ' to ' + orderData.data.to.address;
            
                        middleDiv.html(bottomInfo);
                    
                        var remainingTimeSpan = $('<span></span>').text(' Remaining: ' + orderData.data.left + 's');
                        var timestampSpan = $('<span></span>').text(' Creation: ' + new Date(orderData.data.reg * 1000).toLocaleString());
                        bottomDiv.append(remainingTimeSpan);
                        bottomDiv.append(timestampSpan);
                    
                        orderDataDiv.append(topDiv);
                        orderDataDiv.append(middleDiv);
                        orderDataDiv.append(bottomDiv);
                    
                        // Aggiungi il div dei dati dell'ordine al container della risposta
                        $("#response-container").append(orderDataDiv);
                    }
                }
            
                var newMessage = $("<div></div>").css({
                    "background-color": "#272727",
                    "color": "white",
                    "padding": "5px",
                    "border-radius": "5px",
                    "margin-top": "10px"
                });
                $("#response-container").append(newMessage);
                typeMessage(response.response, newMessage);
                newMessage.after(buttonContainer.clone()); // Append the buttons again after each message
            },
                       
            error: function(xhr, status, error) {
                $("#typing-indicator").addClass("hidden");
                console.error(error);
            }
        });

        $("#user-message").val("");
    });

    // Aggiungi un array per tenere traccia delle valute selezionate
    var selectedCurrencies = [];

    $(document).on('click', '.crypto-item', function() {
        // Se la valuta è già stata selezionata, rimuovila
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            var index = selectedCurrencies.indexOf($(this).data('currency'));
            if (index > -1) {
                selectedCurrencies.splice(index, 1);
            }
        } else {
            // Aggiungi solo se non ci sono più di due valute già selezionate
            if (selectedCurrencies.length < 2) {
                $(this).addClass('selected');
                selectedCurrencies.push($(this).data('currency'));
            }
    
            // Se due valute sono state selezionate, chiudi il modale, svuota l'array e deseleziona tutte le voci
            if (selectedCurrencies.length === 2) {
                closeModal();
                
                selectedCurrenciesFinal = selectedCurrencies;
                // Svuota l'array
                selectedCurrencies = [];
    
                // Deseleziona tutte le voci
                $('.crypto-item.selected').removeClass('selected');
                var i = 0;
                var speed = 30; // tempo in millisecondi per ogni carattere
                let swapMessage = "I want to swap " + selectedCurrenciesFinal[0] + " with " + selectedCurrenciesFinal[1];
                $("#user-message").val("");
                $('#user-message').focus();
                $("#neworder-button").prop("disabled", true);
                $("#orderinfo-button").prop("disabled", true);
                function typeWriter() {
                    if (i < swapMessage.length) {
                        $('#user-message').val($('#user-message').val() + swapMessage.charAt(i));
                        i++;
                        setTimeout(typeWriter, speed);
                    } else {
                        $("#neworder-button").prop("disabled", false);
                        $("#orderinfo-button").prop("disabled", false);
                    }
                }
            
                typeWriter();
            }
        } 
    });
    

    // Event listeners per i pulsanti
    $(document).on('click', '#availability-button', function() {
        // Apri il modal
        openModal();
    });

    $(document).on('click', '#neworder-button', function() {
        $("#orderinfo-button").prop("disabled", true);
        $("#user-message").val("");
        $('#user-message').focus();
        var message = "I want to change ..";
        var i = 0;
        var speed = 30; // tempo in millisecondi per ogni carattere
        function typeWriter() {
            if (i < message.length) {
                $('#user-message').val($('#user-message').val() + message.charAt(i));
                i++;
                setTimeout(typeWriter, speed);
            } else {
                $("#orderinfo-button").prop("disabled", false);
            }
        }
        typeWriter();
    });
    

    $(document).on('click', '#orderinfo-button', function() {
        $("#neworder-button").prop("disabled", true);
        $("#user-message").val("");
        $('#user-message').focus();
        var message = "Give me info about order ID: ";
        var i = 0;
        var speed = 30; // tempo in millisecondi per ogni carattere
    
        function typeWriter() {
            if (i < message.length) {
                $('#user-message').val($('#user-message').val() + message.charAt(i));
                i++;
                setTimeout(typeWriter, speed);
            } else {
                $("#neworder-button").prop("disabled", false);
            }
        }
    
        typeWriter();
    });
    
});




