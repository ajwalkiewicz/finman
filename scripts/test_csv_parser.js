// Test the CSV parsing logic from Transactions.vue
const parseCSVLine = (line) => {
  const result = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      result.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
};

const parseCSV = (csvText) => {
  const lines = csvText.split("\n").filter((line) => line.trim());
  if (lines.length < 2) return [];

  const headers = parseCSVLine(lines[0]).map((h) => h.replace(/"/g, ""));
  const expectedHeaders = [
    "title",
    "origin_account",
    "destination_account",
    "amount",
    "currency",
    "day_of_month",
    "description",
  ];

  // Check if headers match expected format
  const hasValidHeaders = expectedHeaders.every((header) =>
    headers.some((h) => h.toLowerCase() === header.toLowerCase())
  );

  if (!hasValidHeaders) {
    throw new Error(
      `Invalid CSV format. Expected headers: ${expectedHeaders.join(", ")}`
    );
  }

  console.log("Headers found:", headers);

  const data = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]).map((v) => v.replace(/"/g, ""));
    console.log(`Row ${i}: Found ${values.length} values:`, values);

    if (values.length >= headers.length) {
      const row = {};
      headers.forEach((header, index) => {
        const normalizedHeader = header.toLowerCase();
        if (
          expectedHeaders.includes(normalizedHeader) &&
          index < values.length
        ) {
          row[normalizedHeader] = values[index];
        }
      });

      // Only add row if it has the required fields
      if (row.title && row.amount && row.currency && row.day_of_month) {
        data.push(row);
        console.log(`  ✓ Row ${i} added:`, row.title);
      } else {
        console.log(`  ✗ Row ${i} skipped - missing required fields`);
      }
    } else {
      console.log(
        `  ✗ Row ${i} skipped - wrong number of values (expected >= ${headers.length})`
      );
    }
  }

  return data;
};

// Test with the actual CSV data
const csvData = `title,origin_account,destination_account,amount,currency,day_of_month,description
Adam,Income,Millenium,6500,PLN,3,Salary
Isabel,Income,Millenium,8000,PLN,10,Salary
wynagrodzenie,Millenium,Santander,9000,PLN,11,Transfer required by loan
Czynsz - Grafitowa 4/48,Millenium,Expense,"831,68",PLN,4,Rent
Grafitowa 4/48,Millenium,Expense,"214,04",PLN,8,Electricity
16846116,Millenium,Portu,800,PLN,3,Viktors Found
"Adam Walkiewicz, ul Kubusia Puchatka 14/13",Millenium,Expense,49,PLN,8,Internet
Youtube Premium,Millenium,Expense,"18,80",PLN,3,Youtube
Las Ramblas,Santander,Revolut Adam,4000,PLN,13,
Las Ramblas,Revolut Adam,Revolut Together,4000,PLN,14,
Las Ramblas,Revolut Together,Expense,7965,GTQ,16,
Plan Metal,Revolut Adam,Expense,"55,99",PLN,1,Revolut subscription
Lucia Part 1,Millenium,Expense,750,PLN,1,
Lucia Part 2,Millenium,Expense,750,PLN,15,
Loan,Santander,Expense,3800,PLN,15,Loan Payment`;

try {
  console.log("Testing CSV parsing...\n");
  const parsed = parseCSV(csvData);
  console.log(`\n=== RESULTS ===`);
  console.log(`Total transactions parsed: ${parsed.length}`);
  console.log(`Expected: 15 transactions`);
  console.log(`Success: ${parsed.length === 15 ? "✓" : "✗"}`);

  if (parsed.length !== 15) {
    console.log("\nMissing transactions:");
    const csvLines = csvData.split("\n").slice(1);
    csvLines.forEach((line, index) => {
      const values = parseCSVLine(line).map((v) => v.replace(/"/g, ""));
      const title = values[0];
      const found = parsed.some((p) => p.title === title);
      if (!found) {
        console.log(`  - Row ${index + 2}: ${title}`);
      }
    });
  }
} catch (error) {
  console.error("Parsing failed:", error.message);
}
