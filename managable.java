private static final String SLOT_FILE = "DoctorSlots.xlsx";

    public static void addSlots(String doctorId) {
        Scanner sc = new Scanner(System.in);

        try {
            File file = new File(SLOT_FILE);
            Workbook workbook;
            Sheet sheet;

            if (!file.exists()) {
                workbook = new XSSFWorkbook();
                sheet = workbook.createSheet("Slots");
                Row header = sheet.createRow(0);
                header.createCell(0).setCellValue("DoctorID");
                header.createCell(1).setCellValue("Date");
                header.createCell(2).setCellValue("TimeSlot");
            } else {
                FileInputStream fis = new FileInputStream(file);
                workbook = new XSSFWorkbook(fis);
                sheet = workbook.getSheetAt(0);
            }

            boolean adding = true;
            while (adding) {
                System.out.print("Enter available date (YYYY-MM-DD): ");
                String date = sc.nextLine();

                System.out.print("Enter available time slot (e.g. 10:00-11:00): ");
                String timeSlot = sc.nextLine();

                if (isSlotDuplicate(sheet, doctorId, date, timeSlot)) {
                    System.out.println("This slot already exists.");
                } else {
                    int rowNum = sheet.getLastRowNum() + 1;
                    Row row = sheet.createRow(rowNum);
                    row.createCell(0).setCellValue(doctorId);
                    row.createCell(1).setCellValue(date);
                    row.createCell(2).setCellValue(timeSlot);
                    System.out.println("Slot added!");
                }

                System.out.print("Add another slot? (yes/no): ");
                String response = sc.nextLine();
                adding = response.equalsIgnoreCase("yes");
            }

            FileOutputStream fos = new FileOutputStream(SLOT_FILE);
            workbook.write(fos);
            fos.close();
            workbook.close();

        } catch (IOException e) {
            System.out.println("Error writing slots: " + e.getMessage());
        }
    }

    private static boolean isSlotDuplicate(Sheet sheet, String doctorId, String date, String timeSlot) {
        for (Row row : sheet) {
            if (row.getRowNum() == 0) continue;

            String id = row.getCell(0).getStringCellValue();
            String slotDate = row.getCell(1).getStringCellValue();
            String slotTime = row.getCell(2).getStringCellValue();

            if (id.equals(doctorId) && slotDate.equals(date) && slotTime.equals(timeSlot)) {
                return true;
            }
        }
        return false;
    }
