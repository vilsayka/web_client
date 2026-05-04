CREATE TABLE importers (
    id_importer INTEGER PRIMARY KEY REFERENCES users(id_user) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    telephone VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL, 
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_importers_id_importer ON importers(email);

CREATE TABLE orders (
    id_order SERIAL PRIMARY KEY,
    id_customer INTEGER REFERENCES users(id_user) NOT NULL,
    id_importer INTEGER REFERENCES importers(id_importer) NOT NULL,
    date_order DATE NOT NULL,
    date_assembly DATE,
    warranty_period INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_orders_id_customer ON orders(id_customer);
CREATE INDEX idx_orders_id_importer ON orders(id_importer);
CREATE INDEX idx_orders_date_order ON orders(date_order);

CREATE TABLE components (
    id_component SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    warranty_period INTEGER DEFAULT 0,
    price_complete DECIMAL(10, 2) NOT NULL,
    quantity_accessories INTEGER DEFAULT 0,
    code_image BYTEA,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_components_manufacturer ON components(manufacturer);  
CREATE INDEX idx_components_model ON components(model);        
CREATE INDEX idx_components_price ON components(price_complete);

CREATE TABLE component_specs (
    id_spec SERIAL PRIMARY KEY,
    id_component INTEGER UNIQUE REFERENCES components(id_component) ON DELETE CASCADE,
    specifications JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_component_specs_specifications ON component_specs USING GIN (specifications);

CREATE TABLE service_guarantees (
    id_repair_warranty SERIAL PRIMARY KEY,
    id_order INTEGER REFERENCES orders(id_order) NOT NULL,
    id_defective_component INTEGER NOT NULL,
    date_references DATE,
    date_repair_completion DATE,
    Problem_description VARCHAR(300) NOT NULL,
    status_order VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_guarantees_id_order ON service_guarantees(id_order); 
CREATE INDEX idx_guarantees_status ON service_guarantees(status_order);

CREATE TABLE pc_composition (
    id_entry SERIAL PRIMARY KEY,
    id_order INTEGER REFERENCES orders(id_order) NOT NULL,
    id_component INTEGER REFERENCES components(id_component) NOT NULL,
    number_components INTEGER NOT NULL
);

CREATE INDEX idx_composition_id_order ON pc_composition(id_order);    
CREATE INDEX idx_composition_id_component ON pc_composition(id_component);