package vn.edu.hcmuaf.fit.service;

import vn.edu.hcmuaf.fit.dao.AppointmentDAO;
import vn.edu.hcmuaf.fit.model.Appointment;
import vn.edu.hcmuaf.fit.model.Appointment.AppointmentStatus;

import java.util.List;

public class AppointmentService {
    private static AppointmentService instance;

    private AppointmentService() {
    }

    public static AppointmentService getInstance() {
        if (instance == null) {
            instance = new AppointmentService();
        }
        return instance;
    }

    /**
     * Book a new appointment
     * 
     * @param appointment Appointment to book
     * @return generated AppointmentID, or -1 if failed
     */
    public int bookAppointment(Appointment appointment) {
        // TODO: Add validation logic here
        // - Check if datetime is in the future
        // - Check if customer exists
        // - Check for scheduling conflicts (optional)

        return AppointmentDAO.getInstance().createAppointment(appointment);
    }

    /**
     * Get appointment by ID
     */
    public Appointment getAppointment(int appointmentID) {
        return AppointmentDAO.getInstance().getAppointmentById(appointmentID);
    }

    /**
     * Get all appointments for a customer
     */
    public List<Appointment> getCustomerAppointments(int customerID) {
        return AppointmentDAO.getInstance().getAppointmentsByCustomer(customerID);
    }

    /**
     * Update appointment status
     */
    public boolean updateAppointmentStatus(int appointmentID, AppointmentStatus status) {
        return AppointmentDAO.getInstance().updateStatus(appointmentID, status);
    }

    /**
     * Update full appointment
     */
    public boolean updateAppointment(Appointment appointment) {
        return AppointmentDAO.getInstance().updateAppointment(appointment);
    }
}
