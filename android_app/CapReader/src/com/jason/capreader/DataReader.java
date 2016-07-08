
package com.jason.capreader;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Queue;

import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

/**
 * This class implements a runnable interface to keep reading data from local
 * file, and add to queue.
 */
public class DataReader implements Runnable
{

	private String m_strFilePath = "";
	private RandomAccessFile m_raf = null;
	private BufferedWriter m_bw = null;
	private Handler m_uiHandler = null;
	private boolean m_bSave2File = false;
	private Queue<Integer> m_queue = null;

	public static final int VALID_RANGE_LOW = 100;
	public static final int VALID_RANGE_HIGH = 2000;

	public static final String STAT_MAX = "max";
	public static final String STAT_SUM = "sum";
	public static final String STAT_AVG = "avg";

	public DataReader(String strPath, Queue<Integer> que, Handler h, boolean bSave2File)
	{
		m_strFilePath = strPath;
		m_queue = que;
		m_uiHandler = h;
		m_bSave2File = bSave2File;
	}

	@Override
	public void run()
	{
		try
		{
			if (m_raf == null)
			{
				m_raf = new RandomAccessFile(m_strFilePath, "r");
			}

			String strLine = "";
			while (!Thread.currentThread().isInterrupted())
			{
				strLine = m_raf.readLine();
				if (strLine != null)
				{
					// parse values
					String[] items = strLine.split(",");
					int nValidLength = items.length - 1;
					int[] vals = new int[nValidLength];
					for (int i = 0; i < nValidLength; i++)
					{
						vals[i] = Integer.parseInt(items[i]);
					}

					HashMap<String, Integer> hmStat = computeStatics(vals, VALID_RANGE_LOW, VALID_RANGE_HIGH);
					
					// update buffer
					int nVal2Show = hmStat.get(STAT_MAX);
					m_queue.offer(nVal2Show);
					if (m_queue.size() > Common.MAX_DATA_SIZE)
					{
						m_queue.poll();
					}

					// notify UI
					Message msg = m_uiHandler.obtainMessage();
					msg.what = Common.HMSG_NEW_DATA;
					Bundle b = new Bundle();
					b.putInt(Common.DATA_KEY, nVal2Show);
					msg.setData(b);
					m_uiHandler.sendMessage(msg);

					// write to file
					if (m_bSave2File)
					{
						if (m_bw == null)
						{
							SimpleDateFormat dateFormat = new SimpleDateFormat("yyMMdd_HHmmss");
							Date date = new Date();
							String strName = Common.DEFAULT_OUT_DIR + dateFormat.format(date) + "_cap.txt";
							File fOutput = new File(Environment.getExternalStorageDirectory(), strName);
							Log.i(Common.LOG_TAG, "Write to " + fOutput.getAbsolutePath());

							m_bw = new BufferedWriter(new FileWriter(fOutput));
						}

						m_bw.write(strLine);
						m_bw.newLine();

					}

				}
				else
				{
					Log.e(Common.LOG_TAG, String.format("Can not read data from file. file size=%d.", m_raf.length()));
					m_raf.close();
					Thread.sleep(100);
					m_raf = new RandomAccessFile(m_strFilePath, "r");
					continue;
				}
				m_raf.seek(0);
				Thread.sleep(5);

			}
		}
		catch (InterruptedException e)
		{
			Log.e(Common.LOG_TAG, "DataReader is interrupted");
		}
		catch (IOException e)
		{
			Log.e(Common.LOG_TAG, e.getMessage());
		}
		finally
		{
			if (m_raf != null)
			{
				try
				{
					m_raf.close();
					m_raf = null;

					if (m_bw != null)
					{
						m_bw.close();
						m_bw = null;
					}
				}
				catch (IOException e)
				{
					e.printStackTrace();
				}
			}
		}

	}


	public HashMap<String, Integer> computeStatics(int[] arrVals, int nLow, int nHigh)
	{
		HashMap<String, Integer> mpStatics = new HashMap<>();
		int nSum = 0;
		int nMax = 0;
		int nAvg = 0;
		int nValidSensorCount = 0;

		for (int nVal : arrVals)
		{
			if (nVal > nLow && nVal < nHigh)
			{
				nValidSensorCount++;
				nMax = (nVal > nMax) ? nVal : nMax;
				nSum += nVal;
			}
		}
		nAvg = (nValidSensorCount==0) ? 0 : nSum/nValidSensorCount;

		mpStatics.put(STAT_SUM, nSum);
		mpStatics.put(STAT_MAX, nMax);
		mpStatics.put(STAT_AVG, nAvg);

		return mpStatics;

	}

}
