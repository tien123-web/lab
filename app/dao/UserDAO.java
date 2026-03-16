package vn.edu.hcmuaf.fit.dao;

import vn.edu.hcmuaf.fit.db.DBConnect;
import vn.edu.hcmuaf.fit.model.User;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class UserDAO {
    Connection conn = null;
    PreparedStatement ps = null;
    ResultSet rs = null;

    public User checkLogin(String username, String password) {
        try {
            String query = "SELECT * FROM Accounts WHERE Username = ? AND PasswordHash = ? AND Status = 'Active'";
            conn = DBConnect.get();
            ps = conn.prepareStatement(query);
            ps.setString(1, username);
            ps.setString(2, password);
            rs = ps.executeQuery();
            while (rs.next()) {
                return new User(
                        rs.getInt("AccountID"),
                        rs.getString("Username"),
                        rs.getString("PasswordHash"),
                        rs.getString("Email"),
                        rs.getString("Role"),
                        rs.getString("Status"),
                        rs.getTimestamp("CreatedAt"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public boolean checkUserExist(String username) {
        String query = "SELECT * FROM Accounts WHERE Username = ?";
        try {
            conn = DBConnect.get();
            ps = conn.prepareStatement(query);
            ps.setString(1, username);
            rs = ps.executeQuery();
            if (rs.next()) {
                return true;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public boolean checkEmailExist(String email) {
        String query = "SELECT * FROM Accounts WHERE Email = ?";
        try {
            conn = DBConnect.get();
            ps = conn.prepareStatement(query);
            ps.setString(1, email);
            rs = ps.executeQuery();
            if (rs.next()) {
                return true;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public void register(String username, String password, String email) {
        String queryAccount = "INSERT INTO Accounts (Username, PasswordHash, Email, Role, Status) VALUES (?, ?, ?, 'Customer', 'Active')";
        String queryCustomer = "INSERT INTO Customers (AccountID) VALUES (?)";
        try {
            conn = DBConnect.get();
            // Use PreparedStatement with RETURN_GENERATED_KEYS to get the new AccountID
            ps = conn.prepareStatement(queryAccount, java.sql.Statement.RETURN_GENERATED_KEYS);
            ps.setString(1, username);
            ps.setString(2, password);
            ps.setString(3, email);
            ps.executeUpdate();

            // Get the generated AccountID
            rs = ps.getGeneratedKeys();
            if (rs.next()) {
                int accountID = rs.getInt(1);

                // Create corresponding Customer record
                PreparedStatement psCustomer = conn.prepareStatement(queryCustomer);
                psCustomer.setInt(1, accountID);
                psCustomer.executeUpdate();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public int getCustomerIdByAccountId(int accountId) {
        String query = "SELECT CustomerID FROM Customers WHERE AccountID = ?";
        try {
            conn = DBConnect.get();
            ps = conn.prepareStatement(query);
            ps.setInt(1, accountId);
            rs = ps.executeQuery();
            if (rs.next()) {
                return rs.getInt("CustomerID");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1;
    }
}
