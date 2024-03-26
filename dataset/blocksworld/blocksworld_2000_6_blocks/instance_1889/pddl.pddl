

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(on d a)
(ontable e)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a e)
(on c d)
(on e b))
)
)


