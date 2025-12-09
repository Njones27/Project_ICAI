# 3D Print Job Widget Implementation Guide

This guide explains how to implement the 3D print job form widget with backend integration.

## Architecture Overview

The implementation consists of three main components:

1. **Widget Code** (in OpenAI Agent Builder)
2. **Frontend Action Handler** ([managed-chatkit/frontend/src/components/ChatKitPanel.tsx](managed-chatkit/frontend/src/components/ChatKitPanel.tsx))
3. **Backend API Endpoint** ([api/index.py](api/index.py))

## Flow Diagram

```
User fills form → Clicks "Save" → Widget triggers action "lab.job.save"
                                          ↓
                            Frontend handleAction intercepts
                                          ↓
                              POST /api/actions/lab.job.save
                                          ↓
                            Backend processes and saves data
                                          ↓
                              Returns success/error response
                                          ↓
                              Widget shows confirmation
```

## Widget Code (OpenAI Agent Builder)

Place this code in your Agent Builder workflow to create the form widget:

```tsx
<Card
  size="sm"
  asForm
  confirm={{
    label: "Save",
    action: {
      type: "lab.job.save",
    },
  }}
>
  <Col gap={3}>
    <Title value="3D print job" size="sm" />

    <Col gap={1}>
      <Label value="Name" fieldName="user.name" />
      <Input
        name="user.name"
        placeholder="Your name"
        defaultValue={defaultName}
        required
      />
    </Col>

    <Col gap={1}>
      <Label value="Email" fieldName="user.email" />
      <Input
        name="user.email"
        inputType="email"
        placeholder="you@example.com"
        defaultValue={defaultEmail}
        required
      />
    </Col>

    <Row gap={3}>
      <Col gap={1}>
        <Label value="Grams" fieldName="job.grams" />
        <Input
          name="job.grams"
          inputType="number"
          defaultValue={defaultGrams}
          required
        />
      </Col>
      <Col gap={1}>
        <Label value="Time (min)" fieldName="job.timeMin" />
        <Input
          name="job.timeMin"
          inputType="number"
          defaultValue={defaultTimeMin}
          required
        />
      </Col>
    </Row>

    <Checkbox name="job.paid" label="Paid?" defaultChecked={defaultPaid} />
  </Col>
</Card>
```

### Key Widget Properties

- `asForm`: Enables form validation and data collection
- `confirm.action.type`: Custom action type that will be handled by the frontend
- Field names follow the pattern `user.name`, `user.email`, `job.grams`, etc.

## Frontend Implementation

The frontend action handler is in [managed-chatkit/frontend/src/components/ChatKitPanel.tsx](managed-chatkit/frontend/src/components/ChatKitPanel.tsx:12-55).

Key features:
- Intercepts the `lab.job.save` action
- Extracts form data from the action payload
- Sends data to backend API
- Returns success/error response to the widget

The `handleAction` callback is registered with ChatKit via:
```tsx
const chatkit = useChatKit({
  api: { getClientSecret },
  widgets: {
    onAction: handleAction,
  },
});
```

## Backend Implementation

The backend endpoint is at [api/index.py](api/index.py:96-149).

### Endpoint: POST /api/actions/lab.job.save

**Request Body:**
```json
{
  "form_data": {
    "user": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "job": {
      "grams": 150,
      "timeMin": 45,
      "paid": true
    }
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Print job logged successfully for John Doe",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "grams": 150,
    "timeMin": 45,
    "paid": true
  }
}
```

**Error Response (400):**
```json
{
  "error": "Name and email are required"
}
```

### Current Implementation

The current implementation:
- Validates required fields (name, email, grams, timeMin)
- Logs data to console
- Returns success response

### Adding Database Persistence

To save data to a database, replace the TODO section at [api/index.py](api/index.py:132-136) with your database logic:

```python
# Example with SQLite
import sqlite3
from datetime import datetime

# Create connection
conn = sqlite3.connect('print_jobs.db')
cursor = conn.cursor()

# Insert data
cursor.execute('''
    INSERT INTO print_jobs (user_id, name, email, grams, time_min, paid, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (user_id, name, email, grams, time_min, paid, datetime.now()))

conn.commit()
conn.close()
```

Or use an ORM like SQLAlchemy:

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PrintJob(Base):
    __tablename__ = 'print_jobs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    name = Column(String)
    email = Column(String)
    grams = Column(Integer)
    time_min = Column(Integer)
    paid = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

# In your endpoint:
engine = create_engine('sqlite:///print_jobs.db')
Session = sessionmaker(bind=engine)
session = Session()

job = PrintJob(
    user_id=user_id,
    name=name,
    email=email,
    grams=grams,
    time_min=time_min,
    paid=paid
)
session.add(job)
session.commit()
session.close()
```

## Testing

### Local Testing

1. Start the development server:
   ```bash
   cd managed-chatkit/frontend
   npm run dev
   ```

2. In another terminal, start the FastAPI backend:
   ```bash
   pip install fastapi uvicorn httpx
   uvicorn api.index:app --reload
   ```

3. Open your browser and interact with the ChatKit widget

4. Check the backend console for log messages:
   ```
   [3D Print Job] User: John Doe (john@example.com)
   [3D Print Job] Material: 150g, Time: 45min, Paid: True
   [3D Print Job] Session: <session-id>
   ```

### Testing the API Directly

You can test the API endpoint using curl:

```bash
curl -X POST http://localhost:8000/api/actions/lab.job.save \
  -H "Content-Type: application/json" \
  -d '{
    "form_data": {
      "user": {
        "name": "Test User",
        "email": "test@example.com"
      },
      "job": {
        "grams": 100,
        "timeMin": 30,
        "paid": false
      }
    }
  }'
```

## Deployment

The application is configured for Vercel deployment via [vercel.json](vercel.json).

After deployment:
- Frontend will be served from `/`
- API routes will be available at `/api/*`
- The action endpoint will be at `https://your-domain.vercel.app/api/actions/lab.job.save`

## Troubleshooting

### Widget action not firing
- Check browser console for errors
- Verify the action type matches exactly: `"lab.job.save"`
- Ensure `asForm` is set on the Card component

### Backend not receiving data
- Check network tab in browser DevTools
- Verify the endpoint path: `/api/actions/lab.job.save`
- Check CORS configuration in [api/index.py](api/index.py:21-27)

### Form validation errors
- Ensure all required fields have the `required` attribute
- Check field names match the expected structure (`user.name`, `job.grams`, etc.)

## Related Files

- Widget Code: In OpenAI Agent Builder (workflow ID in [workflowCode.py](workflowCode.py:110))
- Frontend Handler: [managed-chatkit/frontend/src/components/ChatKitPanel.tsx](managed-chatkit/frontend/src/components/ChatKitPanel.tsx)
- Backend API: [api/index.py](api/index.py)
- Vercel Config: [vercel.json](vercel.json)

## Next Steps

1. Add database integration to persist form submissions
2. Add authentication/authorization if needed
3. Implement additional endpoints for retrieving saved jobs
4. Add email notifications when jobs are submitted
5. Create admin dashboard to view all submitted jobs
