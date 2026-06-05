-- Demo seed data for HappyRobot Inbound Carrier Sales
-- Apply this once after the API has created the database tables.
--
-- To apply inside the running Postgres container:
--   docker exec -i hr-postgres psql -U happyrobot -d happyrobot < seed_data.sql
--
-- Or if using a different user/db, adjust accordingly.

INSERT INTO loads (id, load_id, origin, destination, pickup_datetime, delivery_datetime, equipment_type, loadboard_rate, notes, weight, commodity_type, num_of_pieces, miles, dimensions, created_at) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'LD-10000', 'Chicago, IL', 'Dallas, TX', '2026-06-06 08:00:00', '2026-06-07 14:00:00', 'Dry Van', 2240.00, 'Call for pickup confirmation.', 32000.0, 'General Freight', 5, 800, '53'' x 102"', '2026-06-04 16:00:00'),
('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'LD-10001', 'Atlanta, GA', 'Charlotte, NC', '2026-06-05 10:00:00', '2026-06-05 18:00:00', 'Dry Van', 681.22, NULL, 39710.0, 'Food Products', 20, 250, '40'' x 97"', '2026-06-04 16:00:00'),
('c3d4e5f6-a7b8-9012-cdef-123456789012', 'LD-10002', 'Los Angeles, CA', 'Phoenix, AZ', '2026-06-07 06:00:00', '2026-06-07 20:00:00', 'Reefer', 1140.00, 'Call for pickup confirmation.', 28000.0, 'Food Products', 12, 380, '48'' x 98"', '2026-06-04 16:00:00'),
('d4e5f6a7-b8c9-0123-def1-234567890123', 'LD-10003', 'Seattle, WA', 'Portland, OR', '2026-06-07 14:00:00', '2026-06-07 22:00:00', 'Dry Van', 483.42, NULL, 28417.0, 'General Freight', 2, 175, '45'' x 99"', '2026-06-04 16:00:00'),
('e5f6a7b8-c9d0-1234-ef12-345678901234', 'LD-10004', 'New York, NY', 'Boston, MA', '2026-06-06 09:00:00', '2026-06-06 16:00:00', 'Flatbed', 559.00, 'Call for pickup confirmation.', 15000.0, 'Building Materials', 8, 215, '53'' x 102"', '2026-06-04 16:00:00'),
('f6a7b8c9-d0e1-2345-f123-456789012345', 'LD-10005', 'Houston, TX', 'New Orleans, LA', '2026-06-07 07:00:00', '2026-06-08 09:00:00', 'Dry Van', 1037.00, NULL, 22000.0, 'Electronics', 15, 350, '50'' x 98"', '2026-06-04 16:00:00'),
('a7b8c9d0-e1f2-3456-a123-567890123456', 'LD-10006', 'Denver, CO', 'Salt Lake City, UT', '2026-06-08 11:00:00', '2026-06-09 04:00:00', 'Step Deck', 1275.00, 'Call for pickup confirmation.', 35000.0, 'Machinery', 3, 425, '53'' x 102"', '2026-06-04 16:00:00'),
('b8c9d0e1-f2a3-4567-b234-678901234567', 'LD-10007', 'Miami, FL', 'Tampa, FL', '2026-06-05 13:00:00', '2026-06-05 19:00:00', 'Dry Van', 560.00, NULL, 18000.0, 'General Freight', 10, 280, '48'' x 96"', '2026-06-04 16:00:00'),
('c9d0e1f2-a3b4-5678-c345-789012345678', 'LD-10008', 'Chicago, IL', 'Dallas, TX', '2026-06-09 15:00:00', '2026-06-10 22:00:00', 'Reefer', 2400.00, NULL, 42000.0, 'Food Products', 18, 800, '53'' x 102"', '2026-06-04 16:00:00'),
('d0e1f2a3-b4c5-6789-d456-890123456789', 'LD-10009', 'Atlanta, GA', 'Charlotte, NC', '2026-06-06 05:00:00', '2026-06-06 13:00:00', 'Flatbed', 750.00, 'Call for pickup confirmation.', 12000.0, 'Building Materials', 6, 250, '45'' x 97"', '2026-06-04 16:00:00'),
('e1f2a3b4-c5d6-7890-e567-901234567890', 'LD-10010', 'Los Angeles, CA', 'Phoenix, AZ', '2026-06-08 09:00:00', '2026-06-08 23:00:00', 'Dry Van', 950.00, NULL, 30000.0, 'General Freight', 14, 380, '53'' x 102"', '2026-06-04 16:00:00'),
('f2a3b4c5-d6e7-8901-f678-012345678901', 'LD-10011', 'Seattle, WA', 'Portland, OR', '2026-06-06 16:00:00', '2026-06-07 00:00:00', 'Reefer', 525.00, 'Call for pickup confirmation.', 22000.0, 'Food Products', 8, 175, '48'' x 98"', '2026-06-04 16:00:00'),
('a3b4c5d6-e7f8-9012-a789-123456789012', 'LD-10012', 'New York, NY', 'Boston, MA', '2026-06-07 11:00:00', '2026-06-07 18:00:00', 'Dry Van', 602.00, NULL, 25000.0, 'Electronics', 4, 215, '40'' x 97"', '2026-06-04 16:00:00'),
('b4c5d6e7-f8a9-0123-b890-234567890123', 'LD-10013', 'Houston, TX', 'New Orleans, LA', '2026-06-06 03:00:00', '2026-06-07 16:00:00', 'Reefer', 755.47, 'Call for pickup confirmation.', 15261.0, 'Machinery', 2, 350, '50'' x 98"', '2026-06-04 16:00:00'),
('c5d6e7f8-a9b0-1234-c901-345678901234', 'LD-10014', 'Denver, CO', 'Salt Lake City, UT', '2026-06-05 18:00:00', '2026-06-06 11:00:00', 'Flatbed', 1190.00, NULL, 33000.0, 'Building Materials', 7, 425, '53'' x 102"', '2026-06-04 16:00:00'),
('d6e7f8a9-b0c1-2345-d012-456789012345', 'LD-10015', 'Miami, FL', 'Tampa, FL', '2026-06-08 07:00:00', '2026-06-08 13:00:00', 'Power Only', 504.00, 'Call for pickup confirmation.', 8000.0, 'General Freight', 1, 280, '40'' x 96"', '2026-06-04 16:00:00'),
('e7f8a9b0-c1d2-3456-e123-567890123456', 'LD-10016', 'Chicago, IL', 'Dallas, TX', '2026-06-05 20:00:00', '2026-06-07 02:00:00', 'Step Deck', 2080.00, NULL, 45000.0, 'Machinery', 3, 800, '53'' x 102"', '2026-06-04 16:00:00'),
('f8a9b0c1-d2e3-4567-f234-678901234567', 'LD-10017', 'Atlanta, GA', 'Charlotte, NC', '2026-06-07 12:00:00', '2026-06-07 20:00:00', 'Power Only', 575.00, 'Call for pickup confirmation.', 9000.0, 'General Freight', 2, 250, '45'' x 97"', '2026-06-04 16:00:00'),
('a9b0c1d2-e3f4-5678-a345-789012345678', 'LD-10018', 'Los Angeles, CA', 'Phoenix, AZ', '2026-06-09 10:00:00', '2026-06-10 00:00:00', 'Flatbed', 1064.00, NULL, 18000.0, 'Building Materials', 9, 380, '48'' x 98"', '2026-06-04 16:00:00'),
('b0c1d2e3-f4a5-6789-b456-890123456789', 'LD-10019', 'Seattle, WA', 'Portland, OR', '2026-06-08 14:00:00', '2026-06-08 22:00:00', 'Step Deck', 595.00, NULL, 27000.0, 'Machinery', 4, 175, '53'' x 102"', '2026-06-04 16:00:00');
