# home-hub
A property management platform that enables landlords to manage properties, units, tenants, leases, payments, and maintenance requests.

## API Endpoints

### Authentication
- `POST /api/register/`
  - Registers a new user.
  - Body fields: `username`, `email`, `password`, `first_name`, `last_name`, `phone_number`
  - Response: created user object (excluding password).

### Users
- `GET /api/users/`
  - Returns a list of users.
  - Requires authentication.

### Organizations
- `GET /api/organizations/`
  - Returns a list of organizations.
  - Requires authentication.
- `POST /api/organizations/`
  - Creates a new organization and assigns the authenticated user as owner.
  - Body fields: `name`
  - Requires authentication.
- `GET /api/organizations/<id>/`
  - Returns organization details.
  - Requires authentication.

### Organization Memberships
- `GET /api/organizations/<organization_pk>/members/`
  - Returns membership records for the organization.
  - Requires authentication.
- `POST /api/organizations/<organization_pk>/members/`
  - Adds a membership to the organization.
  - Body fields: `user`, `role`
  - Requires authentication and owner/admin privileges for the organization.
- `DELETE /api/organizations/<organization_pk>/members/<pk>/`
  - Removes the specified membership.
  - Requires authentication and owner/admin privileges for the organization.

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py test accounts
python manage.py runserver
```

## Notes
- Organization creation automatically creates an `OrganizationMembership` with role `OWNER` for the requesting user.
- Membership creation and deletion require organizational owner/admin access.
