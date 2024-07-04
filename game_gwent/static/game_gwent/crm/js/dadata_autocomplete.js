$(document).ready(function() {
    // Считываем значение API ключа из мета-тега
    var token = $('meta[name="dadata-api-key"]').attr('content');

    console.log("Using DADATA_API_KEY:", token);  // Для отладки

    function enforceRegion(suggestion) {
        var sgt = $("#id_street").suggestions();
        sgt.clear();
        sgt.setOptions({
            token: token,  // Убедитесь, что токен передается здесь
            constraints: {
                locations: { kladr_id: suggestion.data.kladr_id }
            },
            restrict_value: true
        });
    }

    $("#id_region").suggestions({
        token: token,
        type: "ADDRESS",
        bounds: "region",
        geoLocation: false,
        onSelect: enforceRegion
    });

    $("#id_street").suggestions({
        token: token,
        type: "ADDRESS",
        onSelect: function(suggestion) {
            console.log("Selected suggestion:", suggestion);  // Отладка
            $('#id_city').val(suggestion.data.city_with_type || suggestion.data.settlement_with_type || suggestion.data.area_with_type);
            $('#id_region').val(suggestion.data.region_with_type);
            $('#id_postal_code').val(suggestion.data.postal_code);
            $('#id_street').val(suggestion.data.street_with_type || '');  // Добавляем улицу
        }
    });

    $("#id_city").suggestions({
        token: token,
        type: "ADDRESS",
        bounds: "city",
        geoLocation: false,
        onSelect: function(suggestion) {
            console.log("Selected city:", suggestion);  // Отладка
            $('#id_city').val(suggestion.data.city_with_type || suggestion.data.settlement_with_type || suggestion.data.area_with_type);
            $('#id_region').val(suggestion.data.region_with_type);
        }
    });

    $("#id_postal_code").suggestions({
        token: token,
        type: "ADDRESS",
        bounds: "postal_code",
        geoLocation: false,
        onSelect: function(suggestion) {
            console.log("Selected postal code:", suggestion);  // Отладка
            $('#id_postal_code').val(suggestion.data.postal_code);
            $('#id_city').val(suggestion.data.city_with_type || suggestion.data.settlement_with_type || suggestion.data.area_with_type);
            $('#id_region').val(suggestion.data.region_with_type);
            $('#id_street').val(suggestion.data.street_with_type || '');  // Добавляем улицу
        }
    });
});
