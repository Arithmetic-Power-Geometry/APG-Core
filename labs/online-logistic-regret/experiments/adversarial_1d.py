import argparse, math
import numpy as np

def logistic_loss(z, y):
    return np.logaddexp(0.0, -y*z)

def run_sequence(xs, ys, B=5.0, grid_n=1001):
    T=len(xs)
    grid=np.linspace(-B,B,grid_n)
    logw=np.full(grid_n,-math.log(grid_n))
    mix=ons=ogd=0.0
    w_ons=w_ogd=0.0
    A=1.0
    eta_ogd=B/max(1.0,math.sqrt(T))
    alpha=math.exp(-B)/2.0

    for x,y in zip(xs,ys):
        m=logw.max()
        ww=np.exp(logw-m); ww/=ww.sum()
        logits=np.clip(grid*x,-50,50)
        p1=np.sum(ww/(1.0+np.exp(-logits)))
        p1=np.clip(p1,1e-15,1-1e-15)
        z_mix=math.log(p1/(1-p1))
        mix += logistic_loss(z_mix,y)
        logw -= logistic_loss(grid*x,y)

        z=w_ons*x
        ons += logistic_loss(z,y)
        g=-y*x/(1.0+math.exp(float(np.clip(y*z,-50,50))))
        A += g*g
        w_ons=float(np.clip(w_ons-(g/A)/alpha,-B,B))

        z=w_ogd*x
        ogd += logistic_loss(z,y)
        g=-y*x/(1.0+math.exp(float(np.clip(y*z,-50,50))))
        w_ogd=float(np.clip(w_ogd-eta_ogd*g,-B,B))

    comparator=min(float(np.sum(logistic_loss(th*xs,ys))) for th in grid)
    return {"mix":mix-comparator,"ons":ons-comparator,"ogd":ogd-comparator}

def adversarial_search(T,B,trials,seed):
    rng=np.random.default_rng(seed)
    worst=None
    for _ in range(trials):
        xs=rng.choice([-1.0,1.0],T)
        sign=rng.choice([-1.0,1.0])
        ys=np.sign(sign*xs)
        flip_rate=rng.uniform(0.0,0.30)
        ys[rng.random(T)<flip_rate]*=-1
        out=run_sequence(xs,ys,B)
        if worst is None or out["mix"]>worst["mix"]:
            worst=out
    return worst

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--T",nargs="+",type=int,default=[100,300,1000])
    p.add_argument("--B",type=float,default=5.0)
    p.add_argument("--trials",type=int,default=200)
    p.add_argument("--seed",type=int,default=0)
    a=p.parse_args()
    print("T,mix_regret,ons_regret,ogd_regret")
    for T in a.T:
        r=adversarial_search(T,a.B,a.trials,a.seed+T)
        print(f'{T},{r["mix"]:.6f},{r["ons"]:.6f},{r["ogd"]:.6f}')

if __name__=="__main__":
    main()
