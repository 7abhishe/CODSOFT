private static boolean isDuplicateDoctor(String name, long phone) {
    try (FileInputStream fis = new FileInputStream(FILE_NAME);
         Workbook workbook = new XSSFWorkbook(fis)) {

        Sheet sheet = workbook.getSheetAt(0);
        for (Row row : sheet) {
            if (row.getRowNum() == 0) continue; // skip header

            String existingName = row.getCell(1).getStringCellValue();

            // Get phone as long from Excel (stored as numeric)
            Cell phoneCell = row.getCell(4);
            if (phoneCell == null || phoneCell.getCellType() != CellType.NUMERIC) continue;

            long existingPhone = (long) phoneCell.getNumericCellValue();

            if (existingName.equalsIgnoreCase(name) && existingPhone == phone) {
                return true;
            }
        }
    } catch (IOException e) {
        return false;
    }
    return false;
}
