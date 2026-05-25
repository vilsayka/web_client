const specTemplates = {
    "Processor": {
        "cores": "8",
        "threads": "16",
        "socket": "AM4",
        "ram_type": "DDR4",
        "max_ram_gb": "128",
        "max_ram_speed_mhz": "3200",
        "tdp_w": "105",
        "pcie_version": "4.0",
        "max_boost_ghz": "4.1",
        "integrated_graphics": "False"
    },
    "Motherboard": {
        "socket": "AM5",
        "chipset": "B650E",
        "form_factor": "ATX",
        "ram_type": "DDR5",
        "ram_slots": "4",
        "max_ram_gb": "128",
        "max_ram_speed_mhz": "6400",
        "m2_slots": "3",
        "sata_ports": "4",
        "pcie_version": "5.0",
        "usb_c_front": "True",
        "bios_flashback": "True",
        "max_tdp_support_w": "200"
    },
    "Graphics Card": {
        "vram_gb": "24",
        "vram_type": "GDDR6X",
        "tdp_w": "450",
        "length_mm": "348",
        "thickness_slots": "3.5",
        "pcie_version": "4.0",
        "pcie_power_pins": "12VHPWR",
        "recommended_psu_w": "1000"
    },
    "Power Supply": {
        "wattage": "1000",
        "efficiency": "Gold",
        "modular": "Full",
        "form_factor": "ATX",
        "length_mm": "140",
        "cpu_4plus4_count": "2",
        "pcie_8pin_count": "3",
        "pcie_12vhpwr_count": "1",
        "sata_power_count": "8"
    },
    "CPU Cooler": {
        "type": "air",
        "tdp_w": "220",
        "height_mm": "165",
        "fan_count": "2",
        "rgb": "False",
        "ram_clearance_mm": "32",
        "supported_sockets": "LGA1700, LGA1200, AM5, AM4"
    },
    "RAM": {
        "type": "DDR5",
        "total_gb": "32",
        "size_gb_per_stick": "16",
        "stick_count": "2",
        "speed_mhz": "6000",
        "cas_latency": "30",
        "voltage_v": "1.35",
        "rgb": "False",
        "xmp_ready": "True",
        "expo_ready": "True",
        "height_mm": "35"
    },
    "Storage": {
        "type": "NVMe M.2",
        "capacity_gb": "1000",
        "interface": "PCIe 4.0 x4",
        "form_factor": "M.2 2280",
        "read_speed_mbps": "7000",
        "write_speed_mbps": "5000",
        "tbw": "600",
        "dram_cache": "True"
    },
    "Case": {
        "form_factors_supported": "ATX, mATX, ITX",
        "max_gpu_length_mm": "405",
        "max_cpu_cooler_height_mm": "170",
        "max_psu_length_mm": "250",
        "fan_count_included": "3",
        "drive_bays_25": "2",
        "drive_bays_35": "2",
        "psu_form_factors": "ATX",
        "radiator_support": '{"top": "240", "rear": "120", "front": "240/280"}'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('componentType');
    
    if (typeSelect) {
        typeSelect.addEventListener('change', function() {
            const type = this.value;
            const container = document.getElementById('specsContainer');
            
            if (!type || !specTemplates[type]) {
                container.innerHTML = '<textarea name="specifications_json" rows="5" cols="50" placeholder="Характеристики будут сгенерированы автоматически"></textarea>';
                return;
            }
            
            let html = '<div style="border: 1px solid #ccc; padding: 10px; background: #f9f9f9;">';
            html += '<h4>Характеристики для ' + type + ':</h4>';
            
            for (const [key, value] of Object.entries(specTemplates[type])) {
                html += `
                    <div style="margin-bottom: 8px;">
                        <label style="display: inline-block; width: 200px; font-weight: bold;">${key}:</label>
                        <input type="text" name="spec_${key}" value="${value}" style="width: 200px;">
                    </div>
                `;
            }
            
            html += '<input type="hidden" name="specifications_json" id="specsJson">';
            html += '<button type="button" onclick="generateJson()" style="margin-top: 10px;">Собрать в JSON</button>';
            html += '</div>';
            
            container.innerHTML = html;
        });
    }
});

function generateJson() {
    const inputs = document.querySelectorAll('[name^="spec_"]');
    const specs = {};
    
    inputs.forEach(input => {
        const key = input.name.replace('spec_', '');
        let value = input.value;
        
        if (!isNaN(value) && value !== '') {
            if (value.includes('.')) {
                value = parseFloat(value);
            } else {
                value = parseInt(value);
            }
        }
        
        if (value === 'True') value = true;
        if (value === 'False') value = false;
        
        specs[key] = value;
    });
    
    const jsonString = JSON.stringify(specs, null, 2);
    const jsonInput = document.getElementById('specsJson');
    
    if (jsonInput) {
        jsonInput.value = jsonString;
        alert('JSON сгенерирован:\n' + jsonString);
    }
}