import { useEffect } from "react";
import { PatientProps } from "../Types";
import { Button, Table } from "react-bootstrap";
import { usePatient } from "./patientFunction";
import 'bootstrap/dist/css/bootstrap.min.css';

function ShowPatientAppointments({ BACKEND_URL, patientId, refreshAppointments}: PatientProps) {
    const { getPatientAppointments, appointments , cancelAppointment } = usePatient();

    useEffect(() => {
        if (patientId) {
            const url = `${BACKEND_URL}/get_appointments_by_patient_id/${patientId}`;
            getPatientAppointments(url);
        }
    }, [patientId ,refreshAppointments]);

    return (
        <>
            {appointments.length > 0 ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Date</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {appointments.map((appointment, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td>{appointment.date}</td>
                                <td>{appointment.time}</td>
                                {/* <td><Button style={{width: 'fit-content'}} variant="outline-dark" onClick={() => {getDoctordetails()}}>View Details</Button></td> */}
                                <td><Button style={{width: 'fit-content'}} variant="outline-dark" onClick={() => {cancelAppointment(BACKEND_URL , appointment.id)}}>Cancle Appointment</Button></td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            ) : (                  
                <div>
                    <h1>No future appointments</h1>
                </div>
            )}
        </>
    );
}

export default ShowPatientAppointments;
