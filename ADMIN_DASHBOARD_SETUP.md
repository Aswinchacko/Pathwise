# Admin Dashboard Setup Guide

The admin dashboard provides comprehensive management capabilities for the PathWise platform, including user management, system monitoring, and analytics.

## Features

### 🛡️ Admin Dashboard Overview
- **User Management**: View, edit, and manage all users
- **System Health**: Monitor server status and service health
- **Analytics**: View user growth and engagement metrics
- **Activity Monitoring**: Track recent platform activity
- **Role-based Access**: Secure admin-only access

### 📊 Dashboard Sections

#### 1. Overview Tab
- Total users, discussions, and admin statistics
- System health summary
- Quick action buttons
- Recent user registrations

#### 2. User Management Tab
- Paginated user list with search and filters
- Role management (User, Moderator, Admin)
- Account activation/deactivation
- User deletion capabilities

#### 3. System Health Tab
- Server uptime and performance metrics
- Memory usage monitoring
- Database connection status
- Service health checks

#### 4. Recent Activity Tab
- Real-time activity feed
- User registrations and actions
- Discussion creation tracking

#### 5. Analytics Tab
- User growth charts (placeholder for future implementation)
- Engagement metrics
- Platform usage trends

## Setup Instructions

### 1. Database Setup
First, ensure your MongoDB is running and update the User model with admin roles:

```bash
cd auth_back
npm install
```

### 2. Create Admin User
Run the admin seeding script to create the first admin user:

```bash
cd auth_back
npm run seed-admin
```

This creates an admin user with:
- **Email**: admin@pathwise.com
- **Password**: admin123
- **Role**: admin

⚠️ **Important**: Change the password immediately after first login!

### 3. Start the Backend
```bash
cd auth_back
npm run dev
```

### 4. Start the Dashboard
```bash
cd dashboard
npm install
npm run dev
```

### 5. Access Admin Panel
1. Login with the admin credentials
2. Navigate to `/admin` or click "Admin Panel" in the sidebar
3. The admin panel will only be visible to users with admin role

## Admin Features

### User Management
- **Search Users**: Search by name or email
- **Filter Users**: Filter by role (User, Moderator, Admin) and status (Active, Inactive)
- **Edit Roles**: Change user roles directly from the table
- **Toggle Status**: Activate/deactivate user accounts
- **Delete Users**: Remove users from the system (with confirmation)

### System Monitoring
- **Server Health**: Monitor CPU, memory, and uptime
- **Database Status**: Check MongoDB connection
- **Service Status**: Monitor all microservices
- **Performance Metrics**: Track system performance

### Security Features
- **Role-based Access**: Only admin users can access the dashboard
- **Protected Routes**: All admin endpoints require admin authentication
- **Audit Trail**: Track admin actions and user changes
- **Session Management**: Secure token-based authentication

## API Endpoints

### Admin Routes (`/api/admin/`)
- `GET /stats` - Get dashboard statistics
- `GET /users` - Get users with pagination and filters
- `PUT /users/:id` - Update user role or status
- `DELETE /users/:id` - Delete user
- `GET /system/health` - Get system health status
- `GET /activity` - Get recent platform activity
- `GET /analytics` - Get analytics data

### Authentication
All admin routes require:
1. Valid JWT token in Authorization header
2. User role must be 'admin'

Example request:
```javascript
const response = await fetch('/api/admin/stats', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

## User Roles

### User (Default)
- Standard platform access
- Can use all regular features

### Moderator
- Enhanced community management
- Can moderate discussions
- Limited admin capabilities

### Admin
- Full platform access
- User management capabilities
- System administration
- Analytics access

## Security Considerations

### Admin Account Security
1. **Change Default Password**: Immediately change the seeded admin password
2. **Strong Passwords**: Use complex passwords for admin accounts
3. **Limited Admin Users**: Only create admin accounts when necessary
4. **Regular Audits**: Monitor admin activity regularly

### Access Control
- Admin routes are protected by middleware
- Role verification on every request
- Session timeout for security
- Audit logging for admin actions

## Troubleshooting

### Common Issues

#### Admin Panel Not Visible
- Ensure user has admin role in database
- Check JWT token contains correct user data
- Verify admin routes are properly configured

#### Permission Denied
- Confirm user role is 'admin'
- Check JWT token validity
- Ensure backend admin routes are accessible

#### Database Connection Issues
- Verify MongoDB is running
- Check connection string in .env
- Ensure database permissions

### Debug Steps
1. Check browser console for errors
2. Verify network requests in DevTools
3. Check backend logs for authentication errors
4. Confirm user role in database

## Future Enhancements

### Planned Features
- **Advanced Analytics**: Charts and graphs for metrics
- **Bulk User Operations**: Import/export user data
- **System Logs Viewer**: Real-time log monitoring
- **Email Notifications**: Admin alert system
- **Backup Management**: Database backup controls
- **API Rate Limiting**: Request throttling controls

### Integration Opportunities
- **Monitoring Tools**: Integrate with external monitoring
- **Notification Systems**: Slack/Discord integration
- **Audit Systems**: Comprehensive audit logging
- **Reporting**: Automated admin reports

## Support

For issues or questions regarding the admin dashboard:
1. Check this documentation
2. Review backend logs
3. Inspect browser console
4. Verify database connectivity

## Security Warning

⚠️ **Critical**: The admin dashboard provides powerful capabilities. Always:
- Use strong passwords
- Limit admin access
- Monitor admin activity
- Keep the system updated
- Regular security audits

The admin dashboard is a powerful tool for managing the PathWise platform. Use it responsibly and maintain proper security practices.
