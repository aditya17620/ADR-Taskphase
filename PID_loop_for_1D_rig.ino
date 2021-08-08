# include <Wire.h>

float gyro_error =0, g_rawX, g_rawY, g_rawerrorX, g_rawerrorY, g_angleX, g_angleY;
float acc_error =0, a_rawX, a_rawY, a_rawZ, a_rawerrorX, a_rawerrorY, a_angleX, a_angleY;
float total_angleX, total_angleY;
float rad_deg = 180/3.14;
float desired_angle = 0; //desired angle in the X-axis
float Totaltime, DifferenceTime, Previoustime;
float errorX, total_errorX, rate_errorX, last_errorX;
float x_pid, x_pid_p=0, x_pid_i=0, x_pid_d=0;
float defaultval = 1000, motorR, motorL;

void setup()
{
  Serial.begin(9600);
  Totaltime = millis();

  //using the begin command to initiate communication.
  Wire.begin();
  // using the beginTransmission function by specifying the address of the MPU
  Wire.beginTransmission(0x68);
  // using the write function to reset the MPU by placing a 0 in the register 6B
  Wire.write(0x6B);
  Wire.write(0x00);
  // end the transmission so that we can setup the gyro and accelerometer.
  Wire.endTransmission(true);

  // gyroscope setup 
  // initiating the communication to the MPU by specifying the address
  Wire.beginTransmission(0x68);
  // specifying the 1B register which is responsible for the gyroscope values
  Wire.write(0x1B);
  // specifying the sensitivity of the register. The data/command to change the
  // sensitivity can be found on the data sheet. The default dps reading from the gyroscope
  // is 250dps, and can be set by writing 0x00
  Wire.write(0x00);
  // end transmission to the 1B register.
  Wire.endTransmission(true);

  // accelerometer setup
  // initiating the communication to the MPU by specifying the address
  Wire.beginTransmission(0x68);
  // specifying the 1C register which is the register responsible for the accelerometer values.
  Wire.write(0x1C);
  // specifying the sensitivity of the accelerometer. The input value for different ranges
  // can be found in the datasheet. the default range of the accelerometer is +/- 2g.
  // We set this by writing 0x00 using the Wire.write() function
  Wire.write(0x00);
  // end the transmission to the accelerometer register
  Wire.endTransmission(true);


  // estimating the average error of the accelerometer readings to correct the final values
  // this is needed as without the error correction, the angle shown were very off.
  // this loop takes in the first 400 readings of the accelerometer and gyroscope.
  // it then takes the average of all the recorded values to get an estimate of the error.
  // and then corrects the final value before using it for the PID loop.
  // higher the number of itterations, better the accuracy in predicting the error.
  // somehwere between 200 and 500 is a good number of itterations for this purpose.

  // without the error correction, the angles were having a huge drift of around 10 degrees with my MPU
  if(acc_error == 0)
  {
    for(int i=0;i<400;i++)
    {
      //initiating wire communication to the specified address of the MPU.
      Wire.beginTransmission(0x68);
      //requesting data starting from the accelerometerX register, which has the address of 3B
      // according to the MPU 6050 datasheet
      Wire.write(0x3B);
      Wire.endTransmission(false);
      // requesting data from the device that has the address of 68
      // requesting 6 bits of data
      // stopping the request after recieving the specified number of bytes, thereby releasing the bus
      // for other communication.
      Wire.requestFrom(0x68, 6, true);

      // reading the data using the Wire.read function, each value needing two registers.
      // we then divide the data stored by 16384 (based on the range of the accelerometer set
      // previously)
      a_rawX = (Wire.read()<<8|Wire.read())/16384.00;
      a_rawY = (Wire.read()<<8|Wire.read())/16384.00;
      a_rawZ = (Wire.read()<<8|Wire.read())/16384.00;
      
      // using the formula to determine the angle read by the accelerometer.
      // here we calculate the total readings for the 400 itterations, so taht we get a total value
      // to find the average error.
      a_rawerrorX = a_rawerrorX + ((atan((a_rawY)/sqrt(pow(a_rawX,2) + pow(a_rawZ,2)))*rad_deg));
      a_rawerrorY = a_rawerrorY + ((atan(-1*(a_rawX)/sqrt(pow(a_rawY,2) + pow(a_rawZ, 2)))*rad_deg));

      // on the last itteration, we calculate the average of the error by dividing it with 400.
      if (i == 399)
      {
        a_rawerrorX = a_rawerrorX/400;
        a_rawerrorY = a_rawerrorY/400;
        acc_error =1;
      }
    }
  }

  // doing the same thing for the gyroscope sensor, calculating the average error reading.
  if(gyro_error = 0)
  {
    for(int j=0; j<400;j++)
    {
      // initiating the communication to MPU
      Wire.beginTransmission(0x68);
      // requesting data from the register with address 43 and onwards.
      Wire.write(0x43);
      Wire.endTransmission(false);
      // requesting only 4 bytes of data from the registers, and ending the communication
      // after the data transmission ahs been done, so as to release the bus.
      Wire.requestFrom(0x68, 4, true);

      // getting in the raw reading from the registers using the Wire.read function
      // and dividing the total data value based on the dps previously set by us.
      g_rawX = (Wire.read()<<8|Wire.read())/131.0;
      g_rawY = (Wire.read()<<8|Wire.read())/131.0;

      // summing up all the values, to find the average later.
      g_rawerrorX = g_rawerrorX + g_rawX;
      g_rawerrorY = g_rawerrorY + g_rawY;

      // dividing the total value with 400 to find the average error and store it in the same variable
      if(j == 399)
      {
        g_rawerrorX = g_rawerrorX/400;
        g_rawerrorY = g_rawerrorY/400;
        gyro_error = 1;
      }
    }
  }


}

void loop()
{
  // setting the previous time variable to figure out the delta T
  //while calculating the differential error
  Previoustime = Totaltime;
  // keeping track of the total time elapsed since the start of
  // the loop by using the millis function. It stores the data in milliseconds
  Totaltime = millis();
  // calculating the delta T, and then dividing by 1000 to get the time in seconds.
  DifferenceTime = (Totaltime - Previoustime)/1000;

//////////////////////////////////////////////////////////////////////////////////////////////////////

  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 6, true);

  a_rawX = (Wire.read()<<8|Wire.read())/16384.00;
  a_rawY = (Wire.read()<<8|Wire.read())/16384.00;
  a_rawZ = (Wire.read()<<8|Wire.read())/16384.00;
  
  // calculating the angle based on the reading of the rgisters, and then correcting the
  // reading based on the average error calculated from the abover part of the code.
  a_angleX = (atan((a_rawY)/sqrt(pow(a_rawX,2) + pow(a_rawZ,2)))*rad_deg) - a_rawerrorX;
  a_angleY = (atan(-1*(a_rawX)/sqrt(pow(a_rawY,2) + pow(a_rawZ, 2)))*rad_deg) - a_rawerrorY;

//////////////////////////////////////////////////////////////////////////////////////////////////////

  Wire.beginTransmission(0x68);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 4, true);

  // calculating the raw data based off of the readings from the gyroscope alone.
  // it is then error corrected based on the values calculated in the above part of the code
  g_rawX = ((Wire.read()<<8|Wire.read())/131.0) - g_rawerrorX;
  g_rawY = ((Wire.read()<<8|Wire.read())/131.0) - g_rawerrorY;

  // calculating tha angle from the gyroscope. We multiply the time taken between the readings
  // and multiplying it with the raw data from the sensor (after correction).
  // we do this as the data coming from the gyroscope is in degrees per second. To get the degree,
  // we multiply the time (in seconds)
  g_angleX = g_rawX *DifferenceTime;
  g_angleY = g_rawY*DifferenceTime;
  
/////////////////////////////////////////////////////////////////////////////////////////////////////

  // calculating the final angle that we will be using for all calculations
  // based on the combined values from the gyroscope and accelerometer angles.
  // we use a form of a complimentary filter, where the we assign different weightage to the readings
  // from the gyroscope and the accelerometer, to get the most accurate angle values.
  // after checking multiple coefficients, the coefficients that i found worked the best with my
  // MPU6050 are 0.7 and 0.3.
  total_angleX = (0.70 * (total_angleX + g_angleX) + 0.30 * a_angleX);
  total_angleY = 0.70 * (total_angleY + g_angleY) + 0.30 * a_angleY;

  Serial.print("X: ");
  Serial.print(total_angleX);
  Serial.print("       ");
  Serial.print("Y: ");
  Serial.print(total_angleY);
  Serial.print(" ");

/////////////////////////////////////////////////////////////////////////////////////////////////////

  // calculating the net error in the current angle and the desired angle for the 1D rig.
  errorX = total_angleX - desired_angle;
  // integrating the error over a certain time and calculating the total error for the integral control
  total_errorX += errorX*DifferenceTime;
  // differentiating the error to find the error rate that we can use in the differential control
  rate_errorX = (errorX - last_errorX)/DifferenceTime;

  x_pid_p = 1 * errorX;
  x_pid_i = 1* total_errorX; 
  x_pid_d = 1* rate_errorX;

  // calculating the total pid output that will be needed based on the anlge change and desired angle
  x_pid = x_pid_p + x_pid_i + x_pid_d;

  // we can even cap the PID value, but the values the PID was giving at =/- 75 degrees was within 900
  // and -800, so i am not capping the PID values

  // printing out the values for debugging purposes.
  Serial.print("      PID: ");
  Serial.print(x_pid);
  //Serial.println(" ");

  // giving the individual motor commands to both the left and right motors.
  // we add the PID input to the let motor as we need to increase the left motor speed if the 1D rig
  // is pitched downwards to the leftside. Adding the PID output will increase the motor speed
  // on the left and reduce it on the right, causing it to come back to the desired angle.
  // Similarly, if the 1D rig is pitched down towards the rightside, it means that the angle is 
  // in the negative side. So we increase the motor speed on the right side, and reducing the
  // speed on the left side.
  motorL = defaultval + x_pid;
  motorR = defaultval - x_pid;

  // we cap the motor inputs to 1000 and 2000 as anything beyond or below this the motor will not work
  if(motorL > 2000)
  {
    motorL = 2000;
  }
  if(motorL < 1000)
  {
    motorL = 1000;
  }


  if(motorR > 2000)
  {
    motorR = 2000;
  }
  if(motorR < 1000)
  {
    motorR = 1000;
  }

  // printint out the motor speed (in microseconds) to the serial monitor for debugging purposes.
  Serial.print("  MotorR: ");
  Serial.print(motorR);
  Serial.print("  MotorL: ");
  Serial.print(motorL);
  Serial.println(" ");

  
  
}
