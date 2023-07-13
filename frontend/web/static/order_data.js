function createOrderDataDiv(orderData) {
    // Crea un nuovo div per i dati dell'ordine
    var orderDataDiv = $("<div></div>").addClass("order-data-div");
                        
    if (orderData.data) {
        // Crea i div principali
        var topDiv = $("<div></div>").addClass("top-div");
        var bottomDiv = $("<div></div>").addClass("bottom-div");

        // Crea i div per 'from' e 'to'
        var divFrom = $("<div></div>").addClass("div-from");
        var divTo = $("<div></div>").addClass("div-to");

        // Aggiungi le informazioni a 'from' e 'to'
        divFrom.append(
            $("<div></div>").addClass("text").append(
                $("<div></div>").addClass("amount").text("Send " + orderData.data.from.amount + " " + orderData.data.from.symbol + " to"),
                $("<div></div>").addClass("address").text(orderData.data.from.address)
            ),
            $("<div></div>").addClass("svg").html('<img src="https://fixedfloat.com/assets/images/coins/svg/' + orderData.data.from.symbol.toLowerCase() + '.svg" style="width:70px;">')
        );
        divTo.append(
            $("<div></div>").addClass("svg").html('<img src="https://fixedfloat.com/assets/images/coins/svg/' + orderData.data.to.symbol.toLowerCase() + '.svg" style="width:70px;">'),
            $("<div></div>").addClass("text").append(
                $("<div></div>").addClass("amount").text("Receive " + orderData.data.to.amount + " " + orderData.data.to.symbol + " on"),
                $("<div></div>").addClass("address").text(orderData.data.to.address)
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
                $("<div></div>").addClass("content").text(orderData.data.id)
            ),
            $("<div></div>").addClass("time").append(
                $("<div></div>").addClass("title").text('Remaining'),
                $("<div></div>").addClass("content").text(orderData.data.left + 's')
            ),
            $("<div></div>").addClass("creation").append(
                $("<div></div>").addClass("title").text('Creation'),
                $("<div></div>").addClass("content").text(new Date(orderData.data.reg * 1000).toLocaleString())
            )
        );

        divCenter.append(
            $("<div></div>").addClass("text-amount-center").append(
                "Send ",
                $("<span></span>").addClass("amount-center").text(orderData.data.from.amount + ' ' + orderData.data.from.symbol),
                " to the address: "
            ),
            $("<div></div>").addClass("address-center").text(orderData.data.from.address),
            $("<div></div>").addClass("paragraph-center").text('Save the order ID to track the status of your exchange or for support.')
        );        
        
        divRight.append(
            $("<div></div>").addClass("qrcode").html('<img style="width:150px; border-radius: 10px;" src="https://www.investopedia.com/thmb/hJrIBjjMBGfx0oa_bHAgZ9AWyn0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/qr-code-bc94057f452f4806af70fd34540f72ad.png">')
        );

        // Aggiungi 'left', 'center' e 'right' a bottomDiv
        bottomDiv.append(divLeft, divCenter, divRight);

        // Aggiungi topDiv e bottomDiv a orderDataDiv
        orderDataDiv.append(topDiv, bottomDiv);
    }

    return orderDataDiv;
}
