package vn.edu.hcmuaf.fit.service;

import vn.edu.hcmuaf.fit.dao.UserDAO;
import vn.edu.hcmuaf.fit.model.User;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class UserService {
    private static UserService instance;

    public static UserService getInstance() {
        if (instance == null) {
            instance = new UserService();
        }
        return instance;
    }

    private UserService() {
    }

    public User checkLogin(String username, String password) {
        return new UserDAO().checkLogin(username, hashPassword(password));
    }

    public boolean checkUserExist(String username) {
        return new UserDAO().checkUserExist(username);
    }

    public boolean checkEmailExist(String email) {
        return new UserDAO().checkEmailExist(email);
    }

    public void register(String username, String password, String email) {
        new UserDAO().register(username, hashPassword(password), email);
    }

    public String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] messageDigest = md.digest(password.getBytes());
            BigInteger no = new BigInteger(1, messageDigest);
            String hashtext = no.toString(16);
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            return hashtext;
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}
