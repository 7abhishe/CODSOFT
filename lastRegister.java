import java.io.*;
import java.util.*;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.*;

public class RegisterPatient {

    private static final String FILE_NAME = "Patient.xlsx";

    public static void registerPatient() {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter name: ");
        String name = sc.nextLine();

        System.out.print("Enter age: ");
        int age = sc.nextInt();
        sc.nextLine();

        if (age < 0 || age > 120) {
            System.out.println("Invalid age.");
            return;
        }

        System.out.print("Enter phone number: ");
        long phone = 0;
        try {
            phone = Long.parseLong(sc.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Invalid phone number.");
            return;
        }

        if (String.valueOf(phone).length() != 10) {
            System.out.println("Phone number must be 10 digits.");
            return;
        }

        System.out.print("Enter password: ");
        String password = sc.nextLine();

        if (password.length() < 8 || password.length() > 12) {
            System.out.println("Password must be 8–12 characters.");
            return;
        }

        // Generate patient ID (like P001, P002...)
        String id = generatePatientId();

        if (isDuplicate(phone)) {
            System.out.println("❌ Patient already exists.");
            return;
        }

        savePatientToExcel(id, name, age, phone, password);
        System.out.println("✅ Registered successfully! Your ID is: " + id);
    }

    private static boolean isDuplicate(long phone) {
        try (FileInputStream fis = new FileInputStream(FILE_NAME);
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = workbook.getSheetAt(0);
            for (Row row : sheet) {
                if (row.getRowNum() == 0) continue;
                long existingPhone = (long) row.getCell(3).getNumericCellValue();
                if (existingPhone == phone) return true;
            }
        } catch (IOException e) {
            return false; // file doesn't exist yet
        }
        return false;
    }

    private static String generatePatientId() {
        int count = 1;
        try {
            FileInputStream fis = new FileInputStream(FILE_NAME);
            Workbook workbook = new XSSFWorkbook(fis);
            Sheet sheet = workbook.getSheetAt(0);
            count = sheet.getLastRowNum() + 1;
            workbook.close();
        } catch (IOException e) {
            // file not found = start with P001
        }
        return "P" + String.format("%03d", count);
    }

    private static void savePatientToExcel(String id, String name, int age, long phone, String password) {
        try {
            File file = new File(FILE_NAME);
            Workbook workbook;
            Sheet sheet;

            if (!file.exists()) {
                workbook = new XSSFWorkbook();
                sheet = workbook.createSheet("Patients");
                Row header = sheet.createRow(0);
                header.createCell(0).setCellValue("ID");
                header.createCell(1).setCellValue("Name");
                header.createCell(2).setCellValue("Age");
                header.createCell(3).setCellValue("Phone");
                header.createCell(4).setCellValue("Password");
            } else {
                FileInputStream fis = new FileInputStream(file);
                workbook = new XSSFWorkbook(fis);
                sheet = workbook.getSheetAt(0);
            }

            int rowNum = sheet.getLastRowNum() + 1;
            Row row = sheet.createRow(rowNum);
            row.createCell(0).setCellValue(id);
            row.createCell(1).setCellValue(name);
            row.createCell(2).setCellValue(age);
            row.createCell(3).setCellValue(phone);
            row.createCell(4).setCellValue(password);

            FileOutputStream fos = new FileOutputStream(FILE_NAME);
            workbook.write(fos);
            workbook.close();
            fos.close();

        } catch (IOException e) {
            System.out.println("❌ Error writing to Excel: " + e.getMessage());
        }
    }
}
