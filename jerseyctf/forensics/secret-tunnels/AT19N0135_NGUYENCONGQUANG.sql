--Bai 2
CREATE DATABASE QLBANHANG_AT19N0135;
USE QLBANHANG_AT19N0135;
CREATE TABLE KHACHHANG (
    MAKH varchar(5) PRIMARY KEY,
    TENKH nvarchar(30) NOT NULL,
    DIACHI nvarchar(50),
    DT varchar(11),
    EMAIL varchar(30),
    CONSTRAINT CHK_DT_LENGTH CHECK (LEN(DT) BETWEEN 8 AND 11)
);
CREATE TABLE VATTU (
    MAVT varchar(5) PRIMARY KEY,
    TENVT Nvarchar(30) NOT NULL,
    DVT Nvarchar(20),
    GIAMUA Money CHECK (GIAMUA > 0),
    SLTON Int CHECK (SLTON >= 0)
);
CREATE TABLE HOADON (
    MAHD varchar(10) PRIMARY KEY,
    NGAY Date CHECK (NGAY < GETDATE()),
    MAKH varchar(5),
    TONGTG Float,
    FOREIGN KEY (MAKH) REFERENCES KHACHHANG(MAKH)
);
CREATE TABLE CTHD (
    MAHD varchar(10),
    MAVT varchar(5),
    SL int CHECK (SL > 0),
    KHUYENMAI Float,
    GIABAN Float,
    PRIMARY KEY (MAHD, MAVT),
    FOREIGN KEY (MAHD) REFERENCES HOADON(MAHD),
    FOREIGN KEY (MAVT) REFERENCES VATTU(MAVT)
);
INSERT INTO VATTU (MAVT, TENVT, DVT, GIAMUA, SLTON) VALUES
('VT01', N'Xi măng', N'Bao', 50000, 5000),
('VT02', N'Cát', N'Khối', 45000, 50000),
('VT03', N'Gạch ống', N'Viên', 120, 800000),
('VT04', N'Gạch thẻ', N'Viên', 110, 800000),
('VT05', N'Đá lớn', N'Khối', 25000, 100000),
('VT06', N'Đá nhỏ', N'Khối', 33000, 100000),
('VT07', N'Lam gió', N'Cái', 15000, 50000);
INSERT INTO KHACHHANG (MAKH, TENKH, DIACHI, DT, EMAIL) VALUES
('KH01', N'Nguyễn Thị Bé', N'Tân Bình', '38457895', 'bnt@yahoo.com'),
('KH02', N'Lê Hoàng Nam', N'Bình Chánh', '39878987', 'namlehoang@gmail.com'),
('KH03', N'Trần Thị Chiêu', N'Tân Bình', '38457895', NULL),
('KH04', N'Mai Thị Quế Anh', N'Bình Chánh', NULL, NULL),
('KH05', N'Lê Văn Sáng', N'Quận 10', NULL, 'sanglv@hcm.vnn.vn'),
('KH06', N'Trần Hoàng', N'Tân Bình', '38457897', NULL);
INSERT INTO HOADON (MAHD, NGAY, MAKH) VALUES
('HD001', '2010-05-12', 'KH01'),
('HD002', '2010-05-25', 'KH02'),
('HD003', '2010-05-25', 'KH01'),
('HD004', '2010-05-25', 'KH04'),
('HD005', '2010-05-26', 'KH04'),
('HD006', '2010-06-02', 'KH03'),
('HD007', '2010-06-22', 'KH04'),
('HD008', '2010-06-25', 'KH03'),
('HD009', '2010-08-15', 'KH04'),
('HD010', '2010-09-30', 'KH01');
INSERT INTO CTHD (MAHD, MAVT, SL, KHUYENMAI, GIABAN) VALUES
('HD001', 'VT01', 5, NULL, 52000),
('HD001', 'VT05', 10, NULL, 30000),
('HD002', 'VT03', 10000, NULL, 150),
('HD003', 'VT02', 20, NULL, 55000),
('HD004', 'VT03', 50000, NULL, 150),
('HD004', 'VT04', 20000, NULL, 120),
('HD005', 'VT05', 10, NULL, 30000),
('HD005', 'VT06', 15, NULL, 35000),
('HD005', 'VT07', 20, NULL, 17000),
('HD006', 'VT04', 10000, NULL, 120),
('HD007', 'VT04', 20000, NULL, 125),
('HD008', 'VT01', 100, NULL, 55000),
('HD008', 'VT02', 20, NULL, 47000),
('HD009', 'VT02', 25, NULL, 48000),
('HD010', 'VT01', 25, NULL, 57000);
-- Trigger để kiểm tra ràng buộc khóa ngoại
CREATE TRIGGER Check_FK_Constraint
ON CTHD
FOR INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        LEFT JOIN VATTU v ON i.MAVT = v.MAVT
        WHERE v.MAVT IS NULL
    )
    BEGIN
        RAISERROR ('Violation of FOREIGN KEY constraint.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;

-- Trigger để không cho phép CASCADE DELETE trong các ràng buộc khóa ngoại
CREATE TRIGGER Prevent_Cascade_Delete
ON HOADON
INSTEAD OF DELETE
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM deleted d
        JOIN CTHD c ON d.MAHD = c.MAHD
    )
    BEGIN
        RAISERROR ('CASCADE DELETE is not allowed.', 16, 1)
        ROLLBACK TRANSACTION
    END
    ELSE
    BEGIN
        DELETE FROM HOADON WHERE MAHD IN (SELECT MAHD FROM deleted)
    END
END;

-- Trigger để không cho phép user nhập vào hai vật tư có cùng tên
CREATE TRIGGER Prevent_Duplicate_VATTU_Name
ON VATTU
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN VATTU v ON i.TENVT = v.TENVT
    )
    BEGIN
        RAISERROR ('Two VATTU cannot have the same name.', 16, 1)
        ROLLBACK TRANSACTION
    END
    ELSE
    BEGIN
        INSERT INTO VATTU (MAVT, TENVT, DVT, GIAMUA, SLTON)
        SELECT MAVT, TENVT, DVT, GIAMUA, SLTON FROM inserted
    END
END;

-- Trigger để thay đổi KHUYENMAI khi đặt hàng
CREATE TRIGGER Update_KHUYENMAI
ON CTHD
INSTEAD OF INSERT, UPDATE
AS
BEGIN
    DECLARE @SL INT
    SELECT @SL = SL FROM inserted
    IF @SL > 100
        UPDATE CTHD SET KHUYENMAI = 0.05 WHERE SL > 100
    IF @SL > 500
        UPDATE CTHD SET KHUYENMAI = 0.1 WHERE SL > 500
END;

-- Trigger để kiểm tra số lượng tồn và tính lại số lượng tồn
CREATE TRIGGER Check_SLTON_And_Update
ON CTHD
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @SLTON INT, @MAVT VARCHAR(5)
    SELECT @SLTON = SLTON, @MAVT = MAVT FROM inserted
    IF @SLTON >= (SELECT SUM(SL) FROM inserted WHERE MAVT = @MAVT)
    BEGIN
        UPDATE VATTU SET SLTON = @SLTON - (SELECT SUM(SL) FROM inserted WHERE MAVT = @MAVT) WHERE MAVT = @MAVT
        INSERT INTO CTHD (MAHD, MAVT, SL, KHUYENMAI, GIABAN)
        SELECT MAHD, MAVT, SL, KHUYENMAI, GIABAN FROM inserted
    END
    ELSE
    BEGIN
        RAISERROR ('Not enough quantity in stock.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;

-- Trigger để không cho phép user xóa nhiều hơn một vật tư
CREATE TRIGGER Prevent_Multi_Delete_VATTU
ON VATTU
INSTEAD OF DELETE
AS
BEGIN
    IF (SELECT COUNT(*) FROM deleted) > 1
    BEGIN
        RAISERROR ('Cannot delete more than one VATTU at a time.', 16, 1)
        ROLLBACK TRANSACTION
    END
    ELSE
    BEGIN
        DELETE FROM VATTU WHERE MAVT IN (SELECT MAVT FROM deleted)
    END
END;

-- Trigger để kiểm tra số lượng mặt hàng trong một hóa đơn
CREATE TRIGGER Check_Item_Count_Per_Order
ON CTHD
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @MAHD VARCHAR(10)
    SELECT @MAHD = MAHD FROM inserted
    IF (SELECT COUNT(*) FROM CTHD WHERE MAHD = @MAHD) > 5
    BEGIN
        RAISERROR ('Cannot sell more than 5 items per order.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;

-- Trigger để kiểm tra tổng trị giá của một hóa đơn
CREATE TRIGGER Check_Total_Value_Per_Order
ON HOADON
AFTER INSERT, UPDATE
AS
BEGIN
    DECLARE @MAHD VARCHAR(10)
    SELECT @MAHD = MAHD FROM inserted
    IF (SELECT SUM(GIABAN) FROM CTHD WHERE MAHD = @MAHD) > 50000000
    BEGIN
        RAISERROR ('Total value of an order cannot exceed 50000000.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;

-- Trigger để kiểm tra lỗ khi bán hàng
CREATE TRIGGER Check_Loss_Percentage
ON HOADON
AFTER INSERT
AS
BEGIN
    DECLARE @MAHD VARCHAR(10)
    SELECT @MAHD = MAHD FROM inserted
    IF (SELECT SUM(GIABAN - (SELECT GIAMUA FROM VATTU WHERE MAVT = MAVT)) FROM CTHD WHERE MAHD = @MAHD) < -0.5 * (SELECT SUM(GIABAN) FROM CTHD WHERE MAHD = @MAHD)
    BEGIN
        RAISERROR ('Loss exceeds 50%. Cannot sell.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;

-- Trigger để kiểm tra số lượng tồn của mặt hàng Gạch
CREATE TRIGGER Check_Gach_Quantity
ON CTHD
AFTER INSERT
AS
BEGIN
    DECLARE @MAVT VARCHAR(5), @SL INT
    SELECT @MAVT = MAVT, @SL = SL FROM inserted
    IF @MAVT LIKE 'VT04%' AND @SL % 100 <> 0
    BEGIN
        RAISERROR ('Quantity of Gạch must be a multiple of 100.', 16, 1)
        ROLLBACK TRANSACTION
    END
END;
-- Bai 3 
CREATE TABLE Loai (
    MaLoai CHAR(5) PRIMARY KEY,
    TenLoai VARCHAR(255) NOT NULL
);

CREATE TABLE SanPham (
    MaSP CHAR(5) PRIMARY KEY,
    TenSP VARCHAR(255) UNIQUE,
    MaLoai CHAR(5),
    FOREIGN KEY (MaLoai) REFERENCES Loai(MaLoai)
);

CREATE TABLE NhanVien (
    MaNV CHAR(5) PRIMARY KEY,
    HoTen VARCHAR(255) NOT NULL,
    NgaySinh DATE CHECK (DATEDIFF(CURRENT_DATE, NgaySinh) BETWEEN 6570 AND 20140),
    Phai BIT DEFAULT 0
);

CREATE TABLE PhieuXuat (
    MaPX INT AUTO_INCREMENT PRIMARY KEY,
    NgayLap DATE NOT NULL,
    MaNV CHAR(5),
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV)
);

CREATE TABLE CTPX (
    MaPX INT,
    MaSP CHAR(5),
    SoLuong INT CHECK (SoLuong > 0),
    PRIMARY KEY (MaPX, MaSP),
    FOREIGN KEY (MaPX) REFERENCES PhieuXuat(MaPX),
    FOREIGN KEY (MaSP) REFERENCES SanPham(MaSP)
);

INSERT INTO Loai (MaLoai, TenLoai) VALUES
('1', 'Vật liệu xây dựng'),
('2', 'Hàng tiêu dùng'),
('3', 'Ngũ cốc');

INSERT INTO SanPham (MaSP, TenSP, MaLoai) VALUES
('1', 'Xi măng', '1'),
('2', 'Gạch', '1'),
('3', 'Gạo nàng hương', '3'),
('4', 'Bột mì', '3'),
('5', 'Kệ chén', '2'),
('6', 'Đậu xanh', '3');

INSERT INTO NhanVien (MaNV, HoTen, NgaySinh, Phai) VALUES
('NV01', 'Nguyễn Mai Thi', '1982-05-15', '0'),
('NV02', 'Trần Đình Chiến', '1980-12-02', '1'),
('NV03', 'Lê Thị Chi', '1979-01-23', '0');

INSERT INTO PhieuXuat (MaPX, NgayLap, MaNV) VALUES
('1', '2010-03-12', 'NV01'),
('2', '2010-02-03', 'NV02'),
('3', '2010-06-01', 'NV03'),
('4', '2010-06-16', 'NV01');

INSERT INTO CTPX (MaPX, MaSP, SoLuong) VALUES
('1', '1', '10'),
('1', '2', '15'),
('1', '3', '5'),
('2', '2', '20'),
('3', '1', '20'),
('3', '3', '25'),
('4', '5', '12');
--
CREATE TRIGGER MaxCTPXPerPX
BEFORE INSERT ON CTPX
FOR EACH ROW
BEGIN
    DECLARE ct_count INT;
    SELECT COUNT(*) INTO ct_count FROM CTPX WHERE MaPX = NEW.MaPX;
    IF ct_count >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Chỉ cho phép một phiếu xuất có tối đa 5 chi tiết phiếu xuất.';
    END IF;
END;
-- 
CREATE TRIGGER MaxPXPerNVPerDay
BEFORE INSERT ON PhieuXuat
FOR EACH ROW
BEGIN
    DECLARE px_count INT;
    SELECT COUNT(*) INTO px_count FROM PhieuXuat WHERE MaNV = NEW.MaNV AND DATE(NgayLap) = DATE(NEW.NgayLap);
    IF px_count >= 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Một nhân viên chỉ được lập tối đa 10 phiếu xuất trong một ngày.';
    END IF;
END;
-- 
CREATE TRIGGER CheckMaPXExistence
BEFORE INSERT ON CTPX
FOR EACH ROW
BEGIN
    DECLARE px_count INT;
    SELECT COUNT(*) INTO px_count FROM PhieuXuat WHERE MaPX = NEW.MaPX;
    IF px_count = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phiếu xuất này không tồn tại.';
    END IF;
END;
-- Bai 4
CREATE TABLE LOAISP (
    MaLoai INT PRIMARY KEY,
    TenLoai VARCHAR(50) NOT NULL
);

CREATE TABLE SANPHAM (
    MASP INT PRIMARY KEY,
    TenSP VARCHAR(100) NOT NULL,
    Mota TEXT,
    Gia DECIMAL(18,2) NOT NULL,
    Maloai INT,
    FOREIGN KEY (Maloai) REFERENCES LOAISP(MaLoai)
);

CREATE TABLE KHACHHANG (
    MAKH INT PRIMARY KEY,
    TenKH VARCHAR(100) NOT NULL,
    DC VARCHAR(255),
    DT VARCHAR(20)
);

CREATE TABLE DONDH (
    SoDDH INT PRIMARY KEY,
    NgayDat DATE,
    MAKH INT,
    FOREIGN KEY (MAKH) REFERENCES KHACHHANG(MAKH)
);

CREATE TABLE CTDDH (
    SoDDH INT,
    MASP INT,
    SoLuong INT,
    PRIMARY KEY (SoDDH, MASP),
    FOREIGN KEY (SoDDH) REFERENCES DONDH(SoDDH),
    FOREIGN KEY (MASP) REFERENCES SANPHAM(MASP)
);

CREATE TABLE NGUYENLIEU (
    MaNL INT PRIMARY KEY,
    TenNL VARCHAR(100) NOT NULL,
    DVT VARCHAR(20),
    Gia DECIMAL(18,2) NOT NULL
);

CREATE TABLE LAM (
    MaNL INT,
    MASP INT,
    SoLuong INT,
    PRIMARY KEY (MaNL, MASP),
    FOREIGN KEY (MaNL) REFERENCES NGUYENLIEU(MaNL),
    FOREIGN KEY (MASP) REFERENCES SANPHAM(MASP)
);
INSERT INTO LOAISP (MaLoai, TenLoai) VALUES
('L01', 'Tủ'),
('L02', 'Bàn'),
('L03', 'Giường');

INSERT INTO SANPHAM (MASP, TenSP, Mota, Gia, Maloai) VALUES
('SP01', 'Tủ trang điểm', 'Cao 1.4m, rộng 2.2m', 1000000, 'L01'),
('SP02', 'Giường đơn Cali', 'Rộng 1.4m', 1500000, 'L03'),
('SP03', 'Tủ DDA cửa kiếng', 'Cao 1.6m, rộng 2.0m', 800000, 'L01'),
('SP04', 'Bàn ăn', '1m x 1.5m', 650000, 'L02'),
('SP05', 'Bàn uống trà', 'Tròn, 1.8m', 1100000, 'L02');

INSERT INTO KHACHHANG (MAKH, TenKH, DC, DT) VALUES
('KH001', 'Trần Hải Cường', '731 Trần Hưng Đạo, Q.1, TP.HCM', '08-9776655'),
('KH002', 'Nguyễn Thị Bé', '638 Nguyễn Văn Cừ, Q.5, TP.HCM', '0913-666123'),
('KH003', 'Trần Thị Minh Hòa', '543 Mai Thị Lựu, Ba Đình, Hà Nội', '04-9238777'),
('KH004', 'Phạm Đình Tuân', '975 Lê Lai, P.3, TP.Vũng Tàu', '064-543678'),
('KH005', 'Lê Xuân Nguyện', '450 Trưng Vương, Mỹ Tho, Tiền Giang', '073-987123'),
('KH006', 'Văn Hùng Dũng', '291 Hồ Văn Huê, Q.PN, TP.HCM', '08-8222111'),
('KH012', 'Lê Thị Hương Hoa', '980 Lê Hồng Phong, TP.Vũng Tàu', '064-452100'),
('KH016', 'Hà Minh Trí', '332 Nguyễn Thái Học, TP.Quy Nhơn', '056-565656');

INSERT INTO DONDH (SoDDH, NgayDat, MAKH) VALUES
('DH001', '2010-03-15', 'KH001'),
('DH002', '2010-03-15', 'KH016'),
('DH003', '2010-03-16', 'KH003'),
('DH004', '2010-03-16', 'KH012'),
('DH005', '2010-03-17', 'KH001'),
('DH006', '2010-04-01', 'KH002');

INSERT INTO CTDDH (SoDDH, MASP, SoLuong) VALUES
('DH001', 'SP01', 5),
('DH001', 'SP03', 1),
('DH002', 'SP02', 2),
('DH003', 'SP01', 2),
('DH003', 'SP04', 10),
('DH003', 'SP05', 5),
('DH004', 'SP02', 2),
('DH004', 'SP05', 2),
('DH005', 'SP03', 3),
('DH006', 'SP02', 4),
('DH006', 'SP04', 3),
('DH006', 'SP05', 6);

INSERT INTO NGUYENLIEU (MaNL, TenNL, DVT, Gia) VALUES
('NL01', 'Gỗ Lim', 'm3', 1200000),
('NL02', 'Gỗ Sao', 'm3', 1000000),
('NL03', 'Gỗ tạp nham', 'm3', 500000),
('NL04', 'Đinh lớn', 'Kg', 40000),
('NL05', 'Đinh nhỏ', 'Kg', 30000),
('NL06', 'Kiếng', 'm2', 350000);

INSERT INTO LAM (MaNL, MASP, SoLuong) VALUES
('NL01', 'SP01', 1.2),
('NL03', 'SP01', 0.3),
('NL06', 'SP01', 2.5),
('NL02', 'SP02', 1.1),
('NL04', 'SP02', 2.2),
('NL02', 'SP03', 0.9),
('NL05', 'SP03', 2.1),
('NL02', 'SP04', 1.3),
('NL04', 'SP04', 1.7),
('NL03', 'SP05', 0.8),
('NL05', 'SP05', 0.5),
('NL06', 'SP05', 2.4);

CREATE OR REPLACE FUNCTION check_orders_per_day()
RETURNS TRIGGER AS $$
DECLARE
    customer_orders_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO customer_orders_count
    FROM DONDH
    WHERE NgayDat = CURRENT_DATE AND MAKH = NEW.MAKH;

    IF customer_orders_count >= 2 THEN
        RAISE EXCEPTION 'Mỗi khách hàng chỉ được đặt tối đa 2 đơn hàng mỗi ngày';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_per_day_trigger
BEFORE INSERT ON DONDH
FOR EACH ROW
EXECUTE FUNCTION check_orders_per_day();
CREATE OR REPLACE FUNCTION check_order_total_quantity()
RETURNS TRIGGER AS $$
DECLARE
    total_quantity INTEGER;
BEGIN
    SELECT SUM(SoLuong) INTO total_quantity
    FROM CTDDH
    WHERE SoDDH = NEW.SoDDH;

    IF total_quantity > 100 THEN
        RAISE EXCEPTION 'Tổng số lượng sản phẩm trong đơn hàng vượt quá 100';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_total_quantity_trigger
BEFORE INSERT ON CTDDH
FOR EACH ROW
EXECUTE FUNCTION check_order_total_quantity();
CREATE OR REPLACE FUNCTION check_product_profit_margin()
RETURNS TRIGGER AS $$
DECLARE
    product_cost DECIMAL;
    product_price DECIMAL;
BEGIN
    SELECT ng.Gia * l.SoLuong INTO product_cost
    FROM NGUYENLIEU ng
    JOIN LAM l ON ng.MaNL = l.MaNL
    WHERE l.MASP = NEW.MASP;

    SELECT Gia INTO product_price
    FROM SANPHAM
    WHERE MASP = NEW.MASP;

    IF product_price < (product_cost * 1.5) THEN
        RAISE EXCEPTION 'Sản phẩm bị lỗ hơn 50%';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER product_profit_margin_trigger
BEFORE INSERT ON LAM
FOR EACH ROW
EXECUTE FUNCTION check_product_profit_margin();

