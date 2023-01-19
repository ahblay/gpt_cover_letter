/*
$("#generate-latex").click(function() {
    job = $("#job").val()
    cover = $("#cover").val()
    myName = $("#my-name").val()
    myAddress = $("#my-address").val()
    myCity = $("#my-city").val()
    myPhone = $("#my-phone").val()
    myEmail = $("#my-email").val()
    myWebsite = $("#my-website").val()
    recipient = $("#recipient").val()
    company = $("#company").val()
    address = $("#address").val()
    city = $("#city").val()
    completion = $("#completion").val()
    console.log(job)
    console.log(cover)
    console.log([myName, myAddress, myCity, myPhone, myEmail, myWebsite])
    data = {
        "job": job,
        "cover": cover,
        "completion": completion,
        "personal_info": [myName, myAddress, myCity, myPhone, myEmail, myWebsite],
        "business_info": [recipient, company, address, city]
        }
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/generate_latex',
        dataType : 'json',
        async: false,
        data : JSON.stringify(data),
        success : (data) => {
            console.log('isChat response: ' + data)
        },
        error : (data) => {
            console.log(data)
        }
    });
});
*/