function get_color(symbol) {
    // Definisci la mappatura dei colori
    var colorMap = {
        "aave": "#2eb9c7",
        "aaveeth": "#2eb9c7",
        "ada": "#0033ad",
        "adabnb": "#0033ad",
        "adabsc": "#0033ad",
        "atom": "#ffffff",
        "avax": "#e84043",
        "bat": "#e84043",
        "bch": "#85c459",
        "bnb": "#f0b90b",
        "bsc": "#f0b90b",
        "wbnb": "#f0b90b",
        "wbnbbsc": "#f0b90b",
        "btc": "#f7921b",
        "btcbnb": "#f7921b",
        "btcbsc": "#f7921b",
        "btcln": "#5cb4c9",
        "btt": "#ffffff",
        "busd": "f0b90b",
        "busdbsc": "#f0b90b",
        "busdeth": "#f0b90b",
        "busdtrc": "#f0b90b",
        "cake": "#35cfd9",
        "dai": "#f5b730",
        "daibsc": "#f5b730",
        "daieth": "#f5b730",
        "dash": "#018de3",
        "doge": "#bb9e33",
        "dot": "#e7017a",
        "eos": "#c4d4f4",
        "etc": "#8dbd9a",
        "eth": "#557eef",
        "ethbnb": "#557eef",
        "ethbsc": "#557eef",
        "ftm": "#1868ee",
        "kcs": "#41e6af",
        "link": "#2b5adb",
        "ltc": "#2b5adb",
        "mana": "#fb795c",
        "manaeth": "#fb795c",
        "matic": "#8246e4",
        "maticeth": "#8246e4",
        "mkr": "#65c7b4",
        "shib": "#f7921b",
        "shibbsc": "#f7921b",
        "sol": "#65c7b4",
        "ton": "#0088cc",
        "trx": "#ea0028",
        "tusd": "#ffffff",
        "twt": "#2b5adb",
        "twtbsc": "#2b5adb",
        "usdc": "#2675cb",
        "usdcbsc": "#2675cb",
        "usdceth": "#2675cb",
        "usdcmatic": "#2675cb",
        "usdcsol": "#2675cb",
        "usdctrc": "#2675cb",
        "usdp": "#7ccc40",
        "usdt": "#7ac4ad",
        "usdtbnb": "#7ac4ad",
        "usdtbsc": "#7ac4ad",
        "usdtmatic": "#7ac4ad",
        "usdtsol": "#7ac4ad",
        "usdttrc": "#7ac4ad",
        "vet": "#20b3f8",
        "xlm": "#ffffff",
        "xmr": "#fc6404",
        "xrp": "#0fa3db",
        "xtz": "#0fa3db",
        "zec": "#f6c250",
        "zrx": "#ffffff",
        // Aggiungi qui altre coppie simbolo-colore
    };

    // Ottieni il colore corrispondente al simbolo. Se non esiste, restituisci un colore di default (ad es. nero)
    return colorMap[symbol] || "#ffffff";
}

function shortenAddress(address, maxLen) {
    if (address.length > maxLen) {
        var start = address.substring(0, maxLen/3);
        var end = address.substring(address.length - maxLen/3, address.length);
        return start + '...' + end;
    }
    return address;
}

function createOrderDataDiv(orderData) {
    console.log(orderData);
    // Crea un nuovo div per i dati dell'ordine
    var orderDataDiv = $("<div></div>").addClass("order-data-div");
                        
    if (orderData) {
        // Crea i div principali
        var topDiv = $("<div></div>").addClass("top-div");
        var bottomDiv = $("<div></div>").addClass("bottom-div");

        // Crea i div per 'from' e 'to'
        var divFrom = $("<div></div>").addClass("div-from");
        var divTo = $("<div></div>").addClass("div-to");

        // Aggiungi le informazioni a 'from' e 'to'
        divFrom.append(
            $("<div></div>").addClass("text").append(
                $("<div></div>").addClass("amount").text("Send " + orderData.from.amount + " " + orderData.from.coin + " to"),
                $("<div></div>").addClass("address").text(shortenAddress(orderData.from.address, 50))
            ),
            $("<div></div>").addClass("svg").html('<img src="https://fixedfloat.com/assets/images/coins/svg/' + orderData.from.code.toLowerCase() + '.svg" style="width:70px;">')
        );
        divTo.append(
            $("<div></div>").addClass("svg").html('<img src="https://fixedfloat.com/assets/images/coins/svg/' + orderData.to.code.toLowerCase() + '.svg" style="width:70px;">'),
            $("<div></div>").addClass("text").append(
                $("<div></div>").addClass("amount").text("Receive " + orderData.to.amount + " " + orderData.to.coin + " on"),
                $("<div></div>").addClass("address").text(shortenAddress(orderData.to.address, 50))
            )
        );
        
        // Aggiungi 'from' e 'to' a topDiv
        topDiv.append(divFrom, $("<i class='fa-solid fa-angles-right fa-2xl' style='color: #ffffff;'></i>"), divTo);

        // Crea i div per 'left', 'center' e 'right'
        var divLeft = $("<div></div>").addClass("div-left");
        var divCenter = $("<div></div>").addClass("div-center");
        var divRight = $("<div></div>").addClass("div-right");

        // Aggiungi le informazioni a 'left', 'center' e 'right'
        divLeft.append(
            $("<div></div>").addClass("order").append(
                $("<div></div>").addClass("title").text('OrderID'),
                $("<div></div>").addClass("content").text(orderData.id)
            ),
            $("<div></div>").addClass("time").append(
                $("<div></div>").addClass("title").text('Remaining'),
                $("<div></div>").addClass("content").text(orderData.time.left + 's')  // Initial time in seconds
            ),
            $("<div></div>").addClass("creation").append(
                $("<div></div>").addClass("title").text('Creation'),
                $("<div></div>").addClass("content").text(new Date(orderData.time.reg * 1000).toLocaleString())
            )
        );

        var timeLeft = orderData.time.left;
        function updateCountdown() {
            if (timeLeft <= 0) {
                clearInterval(interval);
                $('.time .content').text("Expired");
                return;
            }
        
            var minutes = Math.floor(timeLeft / 60);
            var seconds = timeLeft % 60;
        
            minutes = minutes < 10 ? '0' + minutes : minutes;
            seconds = seconds < 10 ? '0' + seconds : seconds;
        
            $('.time .content').text(minutes + ':' + seconds);
        
            timeLeft--;
        }
        
        var interval = setInterval(updateCountdown, 1000);

        divCenter.append(
            $("<div></div>").addClass("text-amount-center").append(
                "Send ",
                $("<span></span>").addClass("amount-center").text(orderData.from.amount + ' ' + orderData.from.coin),
                " to the address: "
            ),
            $("<div></div>").addClass("address-center").text(orderData.from.address),
            $("<div></div>").addClass("paragraph-center").text('Save the order ID to track the status of your exchange or for support.')
        );   

        setTimeout(function() {
            var color = get_color(orderData.from.code.toLowerCase());
            $('.amount-center').css('color', color);
        }, 0);  
        console.log(orderData);
        divRight.append(
            $("<div></div>").addClass("qrcode").html('<img style="background-color: white; width:150px;" src="' + orderData.qr_data + '">')
        );

        // Aggiungi 'left', 'center' e 'right' a bottomDiv
        bottomDiv.append(divLeft, divCenter, divRight);

        // Aggiungi topDiv e bottomDiv a orderDataDiv
        orderDataDiv.append(topDiv, bottomDiv);
    }

    return orderDataDiv;
}

