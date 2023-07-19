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
    $(document).ready(function() {
        $("#logo").click(function() {
            window.location.href = "/";
        });
    });

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
    var initialMessageContainer = $("<div></div>").addClass("initial-message-container");
    $("#response-container").append(initialMessageContainer);
    typeMessage(initialMessage, initialMessageContainer);

    // Crea i pulsanti
    var button1 = $("<button>📄 Availability</button>").attr('id', 'availability-button').addClass("button-style");
    var button2 = $("<button>✍🏻 New Order</button>").attr('id', 'neworder-button').addClass("button-style");
    var button3 = $("<button>ℹ️ Order Info</button>").attr('id', 'orderinfo-button').addClass("button-style");

    // Crea un contenitore per i pulsanti e aggiungi i pulsanti al contenitore
    var buttonContainer = $("<div></div>").addClass("button-container");

    buttonContainer.hide();
    buttonContainer.append(button1, button2, button3);
    buttonContainer.fadeIn("slow");

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
                    var orderData = JSON.parse(response.order_data);

                    // Utilizza la funzione createOrderDataDiv per creare l'elemento orderDataDiv
                    var orderDataDiv = createOrderDataDiv(orderData);

                    // Aggiungi il div dei dati dell'ordine al container della risposta                       
                    orderDataDiv.hide();
                    $("#response-container").append(orderDataDiv);

                    // Inizia l'animazione del #chat-container
                    $("#chat-container").animate({
                        marginTop: "70px"  // Sostituisci con il valore desiderato
                    }, 2000);  // Durata dell'animazione in millisecondi

                    // Fai il fade in di orderDataDiv
                    orderDataDiv.fadeIn("slow");

                }
                        
                var newMessage = $("<div></div>").addClass("new-message");
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
                let swapMessage = "I want to swap " + selectedCurrenciesFinal[0] + " with " + selectedCurrenciesFinal[1] + " ";
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




