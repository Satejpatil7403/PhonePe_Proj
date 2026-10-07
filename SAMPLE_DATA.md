# Sample PhonePe Transaction Data

This file contains sample transaction formats that the system can parse.

## Format 1: Standard Transaction
```
Date: 09-11-2024
Time: 14:30
Merchant: Amazon Pay
Type: Payment
Amount: ₹1,299.00
Status: Success
Transaction ID: T2024110900001
UPI Ref No: 432198765012
Account: XXXX1234
```

## Format 2: Fuel Transaction
```
Date: 08-11-2024
Time: 10:15
To: Shell Petrol Pump
Direction: Debit
Amount: INR 2,500.00
Status: Completed
Txn ID: T2024110800045
UTR: 431098765098
```

## Format 3: Personal Transfer
```
09/11/2024 | 18:45
Transfer to: John Doe
Via: PhonePe UPI
Amount Paid: Rs. 5,000
Transaction Status: Success
Reference: 432156789023
```

## Format 4: Money Received
```
Date: 07-11-2024
Time: 09:30
From: Salary Account
Type: Credit
Amount: ₹45,000.00
Reference ID: SAL202411070001
UTR Number: 430987654321
Status: Credited
```

## Format 5: Recharge Transaction
```
08-Nov-2024, 16:20
Mobile Recharge
Number: 9876543210
Operator: Airtel
Amount: ₹299
Status: Successful
Transaction ID: T2024110800089
```

## Test Instructions

1. Create a PDF with the above sample transactions
2. Upload through the application
3. Verify that:
   - All transactions are extracted
   - Categories are assigned correctly
   - Amounts are parsed as numbers
   - Dates are in ISO format
   - Insights are generated

## Expected Categorization

- Amazon Pay → shopping
- Shell Petrol Pump → fuel
- John Doe (transfer) → personal_transfer
- Salary Account → personal_transfer (credit)
- Mobile Recharge → recharge
