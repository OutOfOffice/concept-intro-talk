'''
Lovers
Maoya Bassiouni (in progress)
'''


import MySQLdb
from datetime import datetime, timedelta
from numpy import linspace, array
import matplotlib.pyplot as plt
import scipy.stats.mstats
from matplotlib.backends.backend_pdf import PdfPages


class Db(object):
    def __init__(self):
        pass

    def connect(self):
        try:
            con = MySQLdb.connect('localhost', 'maoya', 'maoya_77', \
            		'gmail', unix_socket='/tmp/mysql.sock')
            con.autocommit(True)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return False
        else:
            return con.cursor()

    def make_email_time_series(self, start, end, email):
        cur = self.connect()
        sql = "SELECT date, length, 'DeepSkyBlue' \
        		FROM `from` where from_email='{0}' \
        		AND date BETWEEN '{1}' \
        		AND '{2}' ".format(email, start, end)
        cur.execute(sql)
        from_data = cur.fetchall()
        if from_data != ():
            sql = "SELECT date, length, 'DeepPink' \
            		FROM `to` where to_email='{0}' \
            		AND date BETWEEN '{1}' \
            		AND '{2}' ".format(email, start, end)
            cur.execute(sql)
            to_data = cur.fetchall()
            if to_data != ():
                email_data = []
                email_data.extend(to_data)
                email_data.extend(from_data)
        return email_data


class Visualize(object):
    def __init__(self):
        pass

    def __len_to_size(self, a):
        x = self.qs[0]
        for i, q in enumerate(self.quantiles):
            if a > q:
                x = self.qs[i]
            else:
                break
        return x

    def lovers_plot(self, lover, periods):
        ct = timedelta(seconds=60.*60.*12.)
        db = Db()
        for ind, [start, end] in enumerate(periods):
            emails = db.make_email_time_series(start, end, lover)
            emails = sorted(emails, key=lambda val: val[0], reverse=False)
            dt_data, s_data, c_data = zip(*emails)
            x_data = []
            y_data = []
            for dt in dt_data:
                dt = dt - ct
                dt_str = '%s/%s/%s' % (dt.day, dt.month, dt.year)
                day = datetime.strptime(dt_str, "%d/%m/%Y")
                x_data.append(day)
                y_data.append((dt-day).seconds)

            self.qs = linspace(0.1, 0.9, 9)
            self.quantiles = scipy.stats.mstats.mquantiles(array(s_data), prob=self.qs)
            s_data = map(self.__len_to_size, s_data)

            fig = plt.figure()
            fig.set_size_inches((end - start).days/2., 100)
            ax = fig.add_subplot(111)
            for x, y, c, l in zip(x_data, y_data, c_data, s_data):
                ax.plot(x, y, marker='o', markerfacecolor=c, markeredgecolor='None', \
                		markersize=777 * l, linestyle='', alpha=0.1)

            ax.set_xlim([start-timedelta(days=22), end+timedelta(days=22)])
            ax.set_ylim([-60.* 60. * 10., 60.* 60. * 34.])
            plt.axis('off')
            pdf = PdfPages('/Users/maoya/Desktop/OOO/lovers/Lovers_{0}.pdf'.format(ind+1))
            pdf.savefig(fig)
            pdf.close()


if __name__ == '__main__':

    vz = Visualize()


# test plot lovers................
    periods = [
    		[datetime.strptime('20/07/2010', "%d/%m/%Y"), \
     			datetime.strptime('26/01/2011', "%d/%m/%Y")],
     		[datetime.strptime('27/01/2011', "%d/%m/%Y"), \
     			datetime.strptime('27/08/2011', "%d/%m/%Y")],
     		[datetime.strptime('28/08/2011', "%d/%m/%Y"), \
     			datetime.strptime('04/07/2012', "%d/%m/%Y")],
     		[datetime.strptime('5/07/2012', "%d/%m/%Y"), \
     			datetime.strptime('20/03/2013', "%d/%m/%Y")]
    ]
    
    vz.lovers_plot('bemclaugh@gmail.com', periods)