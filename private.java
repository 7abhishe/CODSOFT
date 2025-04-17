private static void writeDoctorToExcel(Doctor doctor) {
        try {
            File file = new File(FILE_NAME);
            Workbook workbook;
            Sheet sheet;

            if (!file.exists()) {
                workbook = new XSSFWorkbook();
                sheet = workbook.createSheet("Doctors");
                Row header = sheet.createRow(0);
                header.createCell(0).setCellValue("ID");
                header.createCell(1).setCellValue("Name");
                header.createCell(2).setCellValue("Age");
                header.createCell(3).setCellValue("Speciality");
                header.createCell(4).setCellValue("Phone");
                header.createCell(5).setCellValue("Password");
            } else {
                FileInputStream fis = new FileInputStream(file);
                workbook = new XSSFWorkbook(fis);
                sheet = workbook.getSheetAt(0);
            }

            int rowNum = sheet.getLastRowNum() + 1;
            Row row = sheet.createRow(rowNum);

            row.createCell(0).setCellValue(doctor.getId());
            row.createCell(1).setCellValue(doctor.getName());
            row.createCell(2).setCellValue(doctor.getAge());
            row.createCell(3).setCellValue(doctor.getSpeciality());
            row.createCell(4).setCellValue(doctor.getPhone());
            row.createCell(5).setCellValue(doctor.getPassword());

            FileOutputStream fos = new FileOutputStream(FILE_NAME);
            workbook.write(fos);
            fos.close();
            workbook.close();

        } catch (IOException e) {
            System.out.println("Error writing to Excel: " + e.getMessage());
        }
    }
