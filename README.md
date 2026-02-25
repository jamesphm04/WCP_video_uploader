### GET `/api/MVRMedia/GetMVRMedia`

Retrieves all MVRMedia records created after the specified date that have not yet been sent via the API.

#### Parameters

| Parameter  | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| afterDate  | string | Yes      | Filter date (e.g. `2024-01-01`)     |

#### Example Request

```
GET /api/MVRMedia/GetMVRMedia?afterDate=2024-01-01
```

#### Success Response

```json
{
  "status": "success",
  "data": [
    {
      "ID": 1,
      "MVRNumber": "MVR-00123",
      "PhotoGUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "Username": "jsmith",
      "CreatedDateTime": "2024-06-15T10:30:00",
      "FileName": "photo.jpg",
      "FileType": ".jpg"
    }
  ]
}
```

#### Error Response (invalid date)

```json
{
  "status": "error",
  "description": "Invalid date format. Please use a valid date format (e.g., yyyy-MM-dd)."
}
```

#### Notes

- Only returns records where `SentViaAPI IS NULL OR SentViaAPI = 0`.
- Results are ordered by `CreatedDateTime DESC` (newest first).

---

### POST `/api/MVRMedia/SaveMVRMedia`

Saves a base64-encoded image to the server and marks the corresponding database record as sent.

#### Request Body (JSON)

| Field     | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| fileGUID  | string | Yes      | The PhotoGUID of the MVRMedia record     |
| fileName  | string | No       | Desired file name. Defaults to `{fileGUID}.{fileType}` |
| fileType  | string | No       | File extension. Defaults to `.jpg`       |
| imageData | string | Yes      | Base64-encoded image data                |

#### Example Request

```
POST /api/MVRMedia/SaveMVRMedia
Content-Type: application/json

{
  "fileGUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "fileName": "MVR-00123-photo.jpg",
  "fileType": ".jpg",
  "imageData": "/9j/4AAQSkZJRgABAQ..."
}
```

#### Success Response

```json
{
  "status": "success",
  "fileName": "MVR-00123-photo.jpg",
  "filePath": "https://hostname/PickingDataService/Images/MVRMedia/MVR-00123-photo.jpg"
}
```

#### Error Responses

Empty request body:
```json
{
  "status": "error",
  "description": "Request body is empty. Ensure the body contains valid JSON."
}
```

Missing required fields:
```json
{
  "status": "error",
  "description": "fileGUID and imageData are required."
}
```