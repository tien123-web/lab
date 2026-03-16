package vn.edu.hcmuaf.fit.dao;

import vn.edu.hcmuaf.fit.db.DBConnect;
import vn.edu.hcmuaf.fit.model.Appointment;
import vn.edu.hcmuaf.fit.model.Appointment.AppointmentStatus;
import vn.edu.hcmuaf.fit.model.Appointment.AppointmentType;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class AppointmentDAO {
    private static AppointmentDAO instance;

    private AppointmentDAO() {
    }

    public static AppointmentDAO getInstance() {
        if (instance == null) {
            instance = new AppointmentDAO();
        }
        return instance;
    }

    /**
     * Create a new appointment in the database
     * 
     * @param appointment Appointment object to insert
     * @return generated AppointmentID, or -1 if failed
     */
    public int createAppointment(Appointment appointment) {
        Connection conn = DBConnect.get();
        System.out.println("DEBUG: Connection = " + conn);
        if (conn == null) {
            System.out.println("ERROR: Connection is null!");
            return -1;
        }

        String sql = "INSERT INTO appointments (CustomerID, ProductID, AppointmentDateTime, AppointmentType, Address, Status, AdminNote) "
                +
                "VALUES (?, ?, ?, ?, ?, ?, ?)";

        try {
            PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            ps.setInt(1, appointment.getCustomerID());
            System.out.println("DEBUG: CustomerID = " + appointment.getCustomerID());

            if (appointment.getProductID() != null) {
                ps.setInt(2, appointment.getProductID());
            } else {
                ps.setNull(2, Types.INTEGER);
            }
            System.out.println("DEBUG: ProductID = " + appointment.getProductID());

            ps.setTimestamp(3, Timestamp.valueOf(appointment.getAppointmentDateTime()));
            System.out.println("DEBUG: DateTime = " + appointment.getAppointmentDateTime());

            ps.setString(4, appointment.getAppointmentType().getValue());
            System.out.println("DEBUG: Type = " + appointment.getAppointmentType().getValue());

            ps.setString(5, appointment.getAddress());
            System.out.println("DEBUG: Address = " + appointment.getAddress());

            ps.setString(6, appointment.getStatus().getValue());
            System.out.println("DEBUG: Status = " + appointment.getStatus().getValue());

            ps.setString(7, appointment.getAdminNote());
            System.out.println("DEBUG: AdminNote = " + appointment.getAdminNote());

            System.out.println("DEBUG: Executing SQL: " + sql);
            int affectedRows = ps.executeUpdate();
            System.out.println("DEBUG: Affected rows = " + affectedRows);

            if (affectedRows > 0) {
                ResultSet rs = ps.getGeneratedKeys();
                if (rs.next()) {
                    int id = rs.getInt(1);
                    System.out.println("DEBUG: Generated ID = " + id);
                    return id;
                }
            }
        } catch (SQLException e) {
            System.out.println("ERROR: SQLException occurred!");
            System.out.println("ERROR Message: " + e.getMessage());
            System.out.println("ERROR SQLState: " + e.getSQLState());
            System.out.println("ERROR ErrorCode: " + e.getErrorCode());
            e.printStackTrace();
        }
        return -1;
    }

    /**
     * Get appointment by ID
     */
    public Appointment getAppointmentById(int appointmentID) {
        Connection conn = DBConnect.get();
        if (conn == null)
            return null;

        String sql = "SELECT * FROM appointments WHERE AppointmentID = ?";

        try {
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, appointmentID);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                return extractAppointmentFromResultSet(rs);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * Get all appointments for a customer
     */
    public List<Appointment> getAppointmentsByCustomer(int customerID) {
        List<Appointment> appointments = new ArrayList<>();
        Connection conn = DBConnect.get();
        if (conn == null)
            return appointments;

        String sql = "SELECT * FROM appointments WHERE CustomerID = ? ORDER BY AppointmentDateTime DESC";

        try {
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setInt(1, customerID);
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                appointments.add(extractAppointmentFromResultSet(rs));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return appointments;
    }

    /**
     * Update appointment status
     */
    public boolean updateStatus(int appointmentID, AppointmentStatus status) {
        Connection conn = DBConnect.get();
        if (conn == null)
            return false;

        String sql = "UPDATE appointments SET Status = ? WHERE AppointmentID = ?";

        try {
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setString(1, status.getValue());
            ps.setInt(2, appointmentID);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }

    /**
     * Update full appointment details
     */
    public boolean updateAppointment(Appointment appointment) {
        Connection conn = DBConnect.get();
        if (conn == null)
            return false;

        String sql = "UPDATE appointments SET AppointmentDateTime = ?, AppointmentType = ?, " +
                "Address = ?, Status = ?, AdminNote = ? WHERE AppointmentID = ?";

        try {
            PreparedStatement ps = conn.prepareStatement(sql);
            ps.setTimestamp(1, Timestamp.valueOf(appointment.getAppointmentDateTime()));
            ps.setString(2, appointment.getAppointmentType().getValue());
            ps.setString(3, appointment.getAddress());
            ps.setString(4, appointment.getStatus().getValue());
            ps.setString(5, appointment.getAdminNote());
            ps.setInt(6, appointment.getAppointmentID());

            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }

    /**
     * Get all appointments with display info
     */
    public List<Appointment> getAll() {
        return filter(null, null, null, null, null);
    }

    /**
     * Filter appointments
     */
    public List<Appointment> filter(String keyword, String type, String status, String dateFrom, String dateTo) {
        List<Appointment> list = new ArrayList<>();
        Connection conn = DBConnect.get();
        if (conn == null)
            return list;

        StringBuilder sql = new StringBuilder(
                "SELECT a.*, c.FullName, c.PhoneNumber, p.ProductName " +
                        "FROM appointments a " +
                        "JOIN customers c ON a.CustomerID = c.CustomerID " +
                        "LEFT JOIN products p ON a.ProductID = p.ProductID " +
                        "WHERE 1=1 ");

        if (keyword != null && !keyword.isEmpty()) {
            sql.append("AND (a.AppointmentID = ? OR c.FullName LIKE ? OR c.PhoneNumber LIKE ?) ");
        }
        if (type != null && !type.isEmpty()) {
            sql.append("AND a.AppointmentType = ? ");
        }
        if (status != null && !status.isEmpty()) {
            sql.append("AND a.Status = ? ");
        }
        if (dateFrom != null && !dateFrom.isEmpty()) {
            sql.append("AND a.AppointmentDateTime >= ? ");
        }
        if (dateTo != null && !dateTo.isEmpty()) {
            sql.append("AND a.AppointmentDateTime <= ? ");
        }

        sql.append("ORDER BY a.AppointmentDateTime DESC");

        try {
            PreparedStatement ps = conn.prepareStatement(sql.toString());
            int index = 1;

            if (keyword != null && !keyword.isEmpty()) {
                int idTry = -1;
                try {
                    idTry = Integer.parseInt(keyword.replace("#LK", "").trim());
                } catch (Exception e) {
                }
                ps.setInt(index++, idTry);
                ps.setString(index++, "%" + keyword + "%");
                ps.setString(index++, "%" + keyword + "%");
            }
            if (type != null && !type.isEmpty()) {
                ps.setString(index++, type);
            }
            if (status != null && !status.isEmpty()) {
                ps.setString(index++, status);
            }
            if (dateFrom != null && !dateFrom.isEmpty()) {
                ps.setString(index++, dateFrom + " 00:00:00");
            }
            if (dateTo != null && !dateTo.isEmpty()) {
                ps.setString(index++, dateTo + " 23:59:59");
            }

            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                list.add(extractAppointmentFromResultSet(rs));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return list;
    }

    // Stats methods
    public int countAppointmentsToday() {
        String sql = "SELECT COUNT(*) FROM appointments WHERE DATE(AppointmentDateTime) = CURDATE()";
        try {
            PreparedStatement ps = DBConnect.get().prepareStatement(sql);
            ResultSet rs = ps.executeQuery();
            if (rs.next())
                return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public int countNewAppointmentsToday() {
        String sql = "SELECT COUNT(*) FROM appointments WHERE DATE(AppointmentDateTime) = CURDATE() AND Status = 'New'";
        try {
            PreparedStatement ps = DBConnect.get().prepareStatement(sql);
            ResultSet rs = ps.executeQuery();
            if (rs.next())
                return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    public int countConfirmedAppointments() {
        String sql = "SELECT COUNT(*) FROM appointments WHERE Status = 'Confirmed'";
        try {
            PreparedStatement ps = DBConnect.get().prepareStatement(sql);
            ResultSet rs = ps.executeQuery();
            if (rs.next())
                return rs.getInt(1);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }

    /**
     * Helper method to extract Appointment object from ResultSet
     */
    private Appointment extractAppointmentFromResultSet(ResultSet rs) throws SQLException {
        Appointment appointment = new Appointment();
        appointment.setAppointmentID(rs.getInt("AppointmentID"));
        appointment.setCustomerID(rs.getInt("CustomerID"));

        int productID = rs.getInt("ProductID");
        if (!rs.wasNull()) {
            appointment.setProductID(productID);
        }

        Timestamp timestamp = rs.getTimestamp("AppointmentDateTime");
        appointment.setAppointmentDateTime(timestamp.toLocalDateTime());

        appointment.setAppointmentType(AppointmentType.fromString(rs.getString("AppointmentType")));
        appointment.setAddress(rs.getString("Address"));
        appointment.setStatus(AppointmentStatus.fromString(rs.getString("Status")));
        appointment.setAdminNote(rs.getString("AdminNote"));

        // Extra fields
        try {
            appointment.setCustomerName(rs.getString("FullName"));
            appointment.setCustomerPhone(rs.getString("PhoneNumber"));
            appointment.setProductName(rs.getString("ProductName"));
        } catch (SQLException e) {
            // Columns might not exist if using select * from appointments only
            System.out.println("Warning: Display fields missing in ResultSet");
        }

        return appointment;
    }
}
