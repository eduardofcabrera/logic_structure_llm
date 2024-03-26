

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(ontable c)
(on d a)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on a e)
(on b c)
(on c d)
(on e b))
)
)


