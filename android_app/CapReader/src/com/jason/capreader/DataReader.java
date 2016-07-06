
package com.jason.capreader;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.text.SimpleDateFormat;
import java.util.Date;
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

	public static final int VALID_RANGE_LOW = 0;
	public static final int VALID_RANGE_HIGH = 2000;

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

					int nMax = getMaxValues(vals, VALID_RANGE_LOW, VALID_RANGE_HIGH);

					// update buffer
					m_queue.offer(nMax);
					if (m_queue.size() > Common.MAX_DATA_SIZE)
					{
						m_queue.poll();
					}

					// notify UI
					Message msg = m_uiHandler.obtainMessage();
					msg.what = Common.HMSG_NEW_DATA;
					Bundle b = new Bundle();
					b.putInt(Common.DATA_KEY, nMax);
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
							Log.i(Common.LOG_TAG, "Write to " + fOutput.getAbsolutePath() );

							m_bw = new BufferedWriter(new FileWriter(fOutput));
						}
						
						m_bw.write(strLine);
						m_bw.newLine();

					}

				}
				m_raf.seek(0);
				Thread.sleep(10);

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
					
					if(m_bw != null)
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

	/**
	 * Get the max value from array which is among the range of (nLow, nHigh)
	 * 
	 * @param vals
	 * @param nLow
	 * @param nHigh
	 * @return
	 */
	private int getMaxValues(int[] vals, int nLow, int nHigh)
	{
		int nMax = Integer.MIN_VALUE;
		for (int i = 0; i < vals.length; i++)
		{
			if (vals[i] > nLow && vals[i] < nHigh)
			{
				if (vals[i] > nMax)
				{
					nMax = vals[i];
				}
			}

		}
		return nMax;
	}

	public void addData()
	{

	}

}
