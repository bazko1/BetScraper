import matplotlib.pyplot as plt

# x=["10:00","10:15","10:20","10:25","10:30","10:35","10:40","10:45","10:50","10:55","11:00","11:05","11:10"]
# print(len(x))
'zakładamy, że funkcja/metoda przyjmuje liste posortowanych kursów ' \
'od najstarzego kursu do najmłodszego' \
'oraz nazwy druzyn  '

'args = [winHost] , [winAway] , [X]'
def create_plot(host_name, away_name,winHost,winAway,draw=None,result=(None,None) ):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    args=[winHost,winAway]
    if draw:
        args.append(draw)
    
    ax.set_facecolor((0.8, 0.8, 0.8))
    plt.plot(args[0], color='green', marker='o', label=host_name, linewidth=3)
    plt.plot(args[1], color='red', marker='o', label=away_name, linewidth=3)
    plt.ylim(min(min(args[0]), min(args[1])) - 1, max(max(args[0]), max(args[1])) + 1.2)
    if len(args) == 3:
        plt.plot(args[2], color='purple', marker='o', label='X', linewidth=3)
        plt.ylim(min(min(args[0]), min(args[1]), min(args[2])) - 1, max(max(args[0]), max(args[1]), max(args[2])) + 1)

    plt.legend(loc='lower left')
    plt.grid(True)
    desc = host_name + ' - ' + away_name + ' '
    if not None in result: desc += str(result[0]) + ':' + str(result[1])
    fig.canvas.set_window_title( desc )
    plt.show(block=True)
    
